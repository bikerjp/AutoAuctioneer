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
from src.utils import ParseArgs

valid_cmds = ['create_auction', 'edit_auction', 'bid', 'config', 'help']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
db = None
bot = commands.Bot(command_prefix = '!', intents = intents)


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
    del_cmd = True
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
            # reaction to close auction by seller
            await msg.add_reaction("🛑")
            # reaction to get auction end time converted to local tz, open to all
            await msg.add_reaction("🕰️")

        elif 'edit_auction' == args[0]:
            validateCmdChannel(b_cmd, 'edit_auction')
            # retrieve auction from database
            ah_post, post_content = Item.editAuction(discord.utils.get(bot.guilds).id, b_cmd.channel, args)
            await ah_post.edit(content = post_content)

        elif 'bid' == args[0]:
            validateCmdChannel(b_cmd, 'bid')
            ah_post, post_content = Bid.addBid(b_cmd, args, discord.utils.get(bot.guilds).id)
            await ah_post.edit(content = post_content)
            del_cmd = False

        elif 'config' == args[0]:
            config = db.getConfigFile(discord.utils.get(bot.guilds).id)
            config.setConfig(b_cmd.guild, act_args)

        elif 'help' == args[0]:
            # send a DM with bot commands
            p_help = Help()
            await b_cmd.author.send(p_help.printHelp(args))

        else:
            err = ' '
            if len(args) > 0:
                err = err.join(args)
            raise InvalidCommand('Invalid command: ' + err)

    except InvalidCommand as ic:
        await b_cmd.author.send(ic)
        # if not valid cmd, send message to user with list of valid commands
    except Exception as err:
        print ('Caught an unexcepted exception. log and move on. ' + str(err))

    # delete the message to reduce channel clutter, except for bidding on auctions
    if del_cmd:
        await b_cmd.message.delete()


@bot.event
async def on_reaction_add(reaction, user):
    # ignore bot reactions
    if not user.bot:
        record = Item(db.getAuctionRecordFromMsgId(discord.utils.get(bot.guilds).id, reaction.message.id))
        if str(reaction.emoji) == "🛑" and user == reaction.guild.get_member_named(record.auctioneer):
            db.closeAuction(discord.utils.get(bot.guilds).id, record.auction_id)
            await reaction.message.delete()
        elif str(reaction.emoji) == "🕰️":
            await user.send('Auction for: ' + record.item_name + ' by ' + record.auctioneer \
                            +' is ending at ' + str(record.end_date.astimezone(tz = None)))
            await reaction.remove(user)
        else:
            await reaction.remove(user)


if __name__ == "__main__":
    db = AHDatabase()

    bot.run(TOKEN)
