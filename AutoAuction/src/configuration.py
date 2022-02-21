'''
Created on Feb 15, 2022

@author: JP
'''

import discord
from src.utils import InvalidCommand


class Configuration(object):
    '''
    classdocs
    '''

    class AuctionChannel():
        '''
        Contains the paired channel name and unique channel identifier
        '''

        # The name of the chat channel
        name = ''
        # The unique channel id
        id = -1

    channels = {}

    def __init__(self):
        '''
        Constructor - Set the default channel names and ids
        '''
        self.channels['auction_channel'] = type('AuctionChannel', dict(name = 'auction_house'))
        self.channels['bid_channel'] = type('AuctionChannel', dict(name = 'auction_bid'))
        self.channels['chat_channel'] = type('AuctionChannel', dict(name = 'auction_chat'))
        self.channels['trade_channel'] = type('AuctionChannel', dict(name = 'auction_trade_board'))

    def setConfigs(self, guild, chan_args: {}):
        '''
        Updates the auction house channels with the user defined channel names. Will overwrite any
        pre-existing saved channel attributes

        @param[in] guild The discord server
        @param[in] chan_args The dictionary containing the channels to be configured
        '''

        for key, value in chan_args:
            channel = self.AuctionChannel()
            if key in self.channels.keys():
                channel.name = value
                try:
                    channel.id = discord.utils.get(guild.channels, name = value).id
                except:
                    raise InvalidCommand('Invalid channel name. No channel found with name of ' + value)
                self.channels[key] = channel
            else:
                raise InvalidCommand('Invalid channel configuration parameter: ' + key)

    def getActionChannel(self, action):
        act_channel = ''
        if action == 'bid':
            act_channel = self.channels['bid_channel'].name
        elif 'auction' in action:
            act_channel = self.channel['auction_channel'].name

        return act_channel
