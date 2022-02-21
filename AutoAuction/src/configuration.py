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
        chan_name = ''
        # The unique channel id1
        chan_id = -1


        def __init__(self, chan_name = '', chan_id = -1):
            self.chan_name = chan_name
            self.chan_id = chan_id


        def __str__(self):
            return 'chan_name: ' + self.chan_name + ', chan_id: ' + self.chan_id


    channels = {}


    def __init__(self):
        '''
        Constructor - Set the default channel names and ids
        '''
        self.channels['auction_channel'] = self.AuctionChannel('auction-house')
        self.channels['bid_channel'] = self.AuctionChannel('auction-bid')
        self.channels['chat_channel'] = self.AuctionChannel('auction-chat')
        self.channels['trade_channel'] = self.AuctionChannel('auction-trade_board')


    def __str__(self):
        return str(self.channels)


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
                channel.chan_name = value
                try:
                    channel.chan_id = discord.utils.get(guild.channels, name = value).id
                except:
                    raise InvalidCommand('Invalid channel name. No channel found with name of ' + value)
                self.channels[key] = channel
            else:
                raise InvalidCommand('Invalid channel configuration parameter: ' + key)


    def getActionChannel(self, action):
        act_channel = ''
        if action == 'bid':
            act_channel = self.channels['bid_channel'].chan_name
        elif 'auction' in action:
            act_channel = self.channels['auction_channel'].chan_name

        return act_channel
