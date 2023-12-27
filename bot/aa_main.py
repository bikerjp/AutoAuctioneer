'''
Created on Feb 14, 2022

@author: JP
'''

import asyncio
import concurrent.futures
import re
import os
import traceback
from datetime import datetime

import discord
from dotenv import load_dotenv
from discord.ext import commands

from src.database import AHDatabase
from src.bid import Bid
from src.configuration import Configuration
from src.help import Help
from src.item import Item
from src.utils import InvalidCommand
from src.utils import ParseArgs

valid_cmds = ['create_auction', 'edit_auction', 'bid', 'config', 'help']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
db = None
bot = commands.Bot(command_prefix = '-', intents = intents)
__locks = {}

def validateCmdChannel(b_cmd, action):
    config = Configuration(db.getConfigFile(discord.utils.get(bot.guilds).id))
    act_chan = config.getActionChannel(action)
    if b_cmd.message.channel.name != act_chan:
        raise InvalidCommand('Incorrect channel for action. ' + action + ' command is restricted to the channel: ' + act_chan)

@bot.event
async def on_ready():
    # register guild if not already in the database
    db.addNewAuctionHouse(discord.utils.get(bot.guilds))

@bot.command()
async def auction(b_cmd, *args):
    # check b_cmd against list of valid commands
    # if valid cmd, execute cmd
    try:
        act_args = tuple()
        if len(args) == 0:
            raise InvalidCommand('No command arguments given.')
        else:
            act_args = ParseArgs.removeCommand(args)

        if 'create_auction' == args[0]:
            validateCmdChannel(b_cmd, 'create_auction')
            new_auction = Item()
            new_auction.createAuction(str(b_cmd.author), act_args)
            msg = await b_cmd.send(new_auction.createPost(b_cmd.guild))
            new_auction.message_id = msg.id
            db.addAuctionRecord(discord.utils.get(bot.guilds).id, vars(new_auction))
            # create a new lock for the auction
            __locks[discord.utils.get(bot.guilds).id] = {new_auction.auction_id:asyncio.Lock()}
            # reaction to close auction by seller
            await msg.add_reaction("🛑")

        elif 'edit_auction' == args[0]:
            validateCmdChannel(b_cmd, 'edit_auction')
            cmd_args = ParseArgs.tupleToDict(act_args)
            try:
                auction_id = int(cmd_args['auction_id'])
            except:
                raise InvalidCommand('The auction_id argument is missing from command')
            guild = discord.utils.get(bot.guilds)
            await __locks[guild.id][auction_id].acquire()
            # retrieve auction from database
            auction_record = Item(db.getAuctionRecord(guild.id, auction_id))
            if auction_record.auction_id == 0:
                __locks[guild.id][auction_record.auction_id].release()
                raise InvalidCommand('The requested auction does not exist. Auction_id: ' + str(auction_id))
            try:
                ah_post = await b_cmd.channel.fetch_message(auction_record.message_id)
            except:
                raise InvalidCommand(f'Message not found for message id {auction_record.message_id}')
            try:
                auction_record.editAuction(discord.utils.get(bot.guilds).id, cmd_args)
            except:
                __locks[guild.id][auction_record.auction_id].release()
                raise
            __locks[guild.id][auction_record.auction_id].release()
            await ah_post.edit(content = auction_record.createPost(guild))

        elif 'bid' == args[0]:
            validateCmdChannel(b_cmd, 'bid')
            cmd_args = ParseArgs.tupleToDict(act_args)
            try:
                auction_id = int(cmd_args['auction_id'])
            except:
                raise InvalidCommand('The auction_id argument is missing from command')
            guild = discord.utils.get(bot.guilds)
            await __locks[guild.id][auction_id].acquire()
            auction_record = Item(db.getAuctionRecord(guild.id, auction_id))
            if auction_record.auction_id == 0:
                __locks[guild.id][auction_record.auction_id].release()
                raise InvalidCommand('The requested auction does not exist. Auction_id: ' + str(auction_id))
            elif guild.get_member_named(auction_record.auctioneer) == b_cmd.author:
                __locks[guild.id][auction_record.auction_id].release()
                raise InvalidCommand('You cannot bid on your own auction.')
            print(f'auctioneer: {auction_record.auctioneer}, bidder: {b_cmd.author}')
            conf = Configuration(db.getConfigFile(guild.id))
            ah_channel = discord.utils.get(guild.channels, name = conf.channels['auction_channel'].chan_name)
            ah_post = await ah_channel.fetch_message(auction_record.message_id)
            try:
                post_content, bid_post, last_bidder, cancel = Bid.addBid(b_cmd, cmd_args, guild.id, auction_record, ah_post.content)
            except:
                __locks[guild.id][auction_record.auction_id].release()
                raise
            __locks[guild.id][auction_record.auction_id].release()
            await ah_post.edit(content = post_content)
            await b_cmd.send(bid_post)

            # do not update posts or send messages if bidder is leaving the auction
            '''
            while bid_post != '':
                await ah_post.edit(content = post_content)
                await b_cmd.send(bid_post)
                await __locks[guild.id][auction_record.auction_id].acquire()
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    autobid = executor.submit(Bid.autoUpdateBid, guild.id, auction_record, ah_post.content)
                    post_content, bid_post, last_bid = autobid.result()
                __locks[guild.id][auction_record.auction_id].release()
                # do not auto update again for another second. Allow other bidders to enter a bid.
                await asyncio.sleep(1)
            '''
        elif 'config' == args[0]:
            config = db.getConfigFile(discord.utils.get(bot.guilds).id)
            allowed = False
            for role in config.auth_roles:
                if role in b_cmd.author.roles:
                    allowed = True
                    break
            if b_cmd.author.id == b_cmd.guild.owner.id or allowed:
                conf_args = ParseArgs.tupleToDict(act_args)
                config.setConfig(b_cmd.guild, conf_args)
                db.setConfigFile(discord.utils.get(bot.guilds).id, config.toDict())
            else:
                await b_cmd.guild.owner.send(f'Unauthorized user [{b_cmd.author}] attempted to change the AutoAuctioneer configuration parameters.')

        elif 'help' == args[0]:
            # send a DM with bot commands
            p_help = Help()
            await b_cmd.author.send(p_help.printHelp(act_args))

        else:
            err = ' '
            if len(args) > 0:
                err = err.join(args)
            raise InvalidCommand('Invalid command: ' + err)

    except InvalidCommand as ic:
        await b_cmd.author.send(ic)
    except:
        traceback.print_exc()
        # if not valid cmd, send message to user with list of valid commands
#    except Exception as err:
#        print ('Caught an unexcepted exception. log and move on. ' + str(err))

    # delete the message to reduce channel clutter, except for bidding on auctions
    await b_cmd.message.delete()

@bot.event
async def on_reaction_add(reaction, user):
    # ignore bot reactions
    if not user.bot:
        this_guild = discord.utils.get(bot.guilds)
        conf = Configuration(db.getConfigFile(this_guild.id))
        if reaction.message.channel == discord.utils.get(this_guild.channels, name = conf.channels['auction_channel'].chan_name):
            try:
                auction_id = int(re.search(r'.*Auction id: ([0-9]+).*', reaction.message.content).group(1))
            except:
                raise InvalidCommand('No action id found for message id: ' + str(reaction.message.id))
            record = Item(db.getAuctionRecord(this_guild.id, auction_id))
            if str(reaction.emoji) == "🛑" and user == this_guild.get_member_named(record.auctioneer):
                cancelled = db.closeAuction(this_guild.id, record.auction_id)
                if not cancelled:
                    bid_match = re.search(r'.*Current bid:(.*\>) ([0-9. ]+gp).*', reaction.message.content)
                    if bid_match:
                        close_msg = user.mention + ' selling ' + record.item_name + ' to ' + bid_match.group(1)\
                                    +' for ' + bid_match.group(2)
                        trade_board = discord.utils.get(this_guild.channels, name = conf.channels['trade_channel'].chan_name)
                        await trade_board.send(close_msg)
                    else:
                        await user.send('Auction closed for ' + record.item_name + ' with no bids placed')
                await reaction.message.delete()
            else:
                await reaction.remove(user)

if __name__ == "__main__":
    db = AHDatabase()

    try:
        bot.run(TOKEN)
    except:
        traceback.print_exc()
