'''
Created on Feb 14, 2022

@author: JP
'''

import discord
import os
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from src.database import AHDatabase
from src.bid import Bid
from src.configuration import Configuration
from src.help import Help
from src.item import Item
from src.utils import InvalidCommand

valid_cmds = ['create_auction', 'edit_auction', 'cancel_auction', 'bid', 'config', 'help']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
db = None
bot = commands.Bot(command_prefix = '!', intents = intents)


def validateCmdChannel(b_cmd, action):
    config = db.getConfigFile(discord.utils.get(bot.guilds).id)
    act_chan = config.getActionChannel(action)
    if b_cmd.message.channel.name != act_chan:
        raise InvalidCommand('Incorrect channel for action. ' + action + ' command is restricted to the channel: ' + act_chan)


@bot.event
async def on_ready():
    # register guild if not already in the database
    db.addNewAuctionHouse(discord.utils.get(bot.guilds))


@bot.command()
async def parseCommand(b_cmd, *args):
    # check b_cmd against list of valid commands
    # if valid cmd, execute cmd
    try:
        if 'create_auction' in args:
            validateCmdChannel(b_cmd)
            new_auction = Item()
            new_auction.createAuction(b_cmd.author, args)
            db.addAuctionRecord(discord.utils.get(bot.guilds).id, new_auction)
            msg = await b_cmd.send(new_auction.createPost(b_cmd.guild))
            # reaction to close auction by seller
            await msg.add_reaction("🛑")
            # reaction to get auction end time converted to local tz, open to all
            await msg.add_reaction("🕰️")

        elif 'edit_auction' in args:
            validateCmdChannel(b_cmd)
            # retrieve auction from database
            record = db.getAuctionRecord(discord.utils.get(bot.guilds).id, b_cmd.message.id)
            if record:
                ah_post = b_cmd.channel.fetch_message(record.message_id)
                record.updateAuction(args, ah_post)
                db.addAuctionRecord(discord.utils.get(bot.guilds).id, record)
                await ah_post.edit(content = new_auction.createPost(b_cmd.guild))

        elif 'cancel_auction' in args:
            validateCmdChannel(b_cmd)
            db.cancelAuction(args)

        elif 'bid' in args:
            validateCmdChannel(b_cmd)
            bid = Bid()
            bid.addNewBid(b_cmd, *args, db.getNextBidID())

        elif 'config' in args:
            config = db.getConfigFile(discord.utils.get(bot.guilds).id)
            config.setConfig(b_cmd.guild, args)

        elif 'help' in args:
            # send a DM with bot commands
            p_help = Help()
            await b_cmd.author.send(p_help.printHelp(args))

        else:
            raise InvalidCommand('Invalid command: '.join(args))
    except InvalidCommand as ic:
        await b_cmd.author.send(ic)
        # if not valid cmd, send message to user with list of valid commands
    except:
        print ('Caught an unexcepted exception. log and move on.')

    # delete the message to reduce channel clutter, except for bidding on auctions
    if 'bid' not in args:
        await b_cmd.message.delete()


@bot.event
async def on_reaction_add(reaction, user):
    record = db.getAuctionRecord(discord.utils.get(bot.guilds).id, reaction.message.id)
    if reaction == "🛑" and user == reaction.guild.get_member_named(record.auctioneer):
        db.closeAuction(discord.utils.get(bot.guilds).id, record.auction_id)
        await reaction.message.delete()
    elif reaction == "🕰️":
        local_time = datetime.now()
        await user.send(local_time)
        await reaction.remove(user)
    else:
        await reaction.remove(user)


if __name__ == "main":
    db = AHDatabase()

    print ('before bot run')
    bot.run(TOKEN)
    print ('after bot run')
