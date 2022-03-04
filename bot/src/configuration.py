'''
Created on Feb 15, 2022

@author: JP
'''

import re
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


        def __init__(self, in_dict = {}):
            if len(in_dict) > 0:
                for k, v in in_dict.items():
                    setattr(self, k, v)
            else:
                self.chan_name = ''
                self.chan_id = -1


    channels = {}
    auth_roles = []
    purge_auction = False
    bidder_overwrite = False


    def __init__(self, in_dict = {'':{}}):
        '''
        Constructor - Set the default channel names and ids
        '''
        if len(in_dict) > 0 and '' not in in_dict.keys():
            for k, v in in_dict.items():
                if k == 'auth_roles':
                    self.auth_roles = v.split(',')
                elif k == 'purge_auction':
                    self.purge_auction = v
                elif k == 'bidder_overwrite':
                    self.bidder_overwrite = v
                else:
                    self.channels[k] = self.AuctionChannel(v)
        else:
            self.channels['auction_channel'] = self.AuctionChannel({'chan_name':'auction-house', 'chan_id':-1})
            self.channels['bid_channel'] = self.AuctionChannel({'chan_name':'auction-bid', 'chan_id':-1})
            self.channels['chat_channel'] = self.AuctionChannel({'chan_name':'auction-chat', 'chan_id':-1})
            self.channels['trade_channel'] = self.AuctionChannel({'chan_name':'auction-trade-board', 'chan_id':-1})
            self.auth_roles = []
            self.purge_auction = False
            self.bidder_overwrite = False


    def toDict(self):
        ret_dict = {}
        for key in self.channels.keys():
            ret_dict[key] = vars(self.channels[key])
        ret_dict['auth_roles'] = ','.join(self.auth_roles)
        ret_dict['purge_auction'] = self.purge_auction
        ret_dict['bidder_overwrite'] = self.bidder_overwrite
        return ret_dict


    def setConfigs(self, guild, conf_args: {}):
        '''
        Updates the auction house channels with the user defined channel names. Will overwrite any
        pre-existing saved channel attributes

        @param[in] guild The discord server
        @param[in] conf_args The dictionary containing the channels to be configured
        '''

        for key, value in conf_args:
            channel = self.AuctionChannel()
            if key in self.channels.keys():
                channel.chan_name = value
                try:
                    channel.chan_id = discord.utils.get(guild.channels, name = value).id
                except:
                    raise InvalidCommand('Invalid channel name. No channel found with name of ' + value)
                self.channels[key] = channel
            elif key == 'auth_roles':
                self.auth_roles = re.sub(',[ ]*', ',', value).split(', ')
            elif key == 'purge_auction':
                try:
                    self.purge_auction = distutils.util.strtobool(value)
                except ValueError as err:
                    raise InvalidCommand('Invalid argument for purge_auction: ' + err + '. Must be a true/false or yes/no, case insensitive.')
            elif key == 'bidder_overwrite':
                try:
                    self.bidder_overwrite = distutils.util.strtobool(value)
                except ValueError as err:
                    raise InvalidCommand('Invalid argument for bidder_overwrite: ' + err + '. Must be a true/false or yes/no, case insensitive.')
            else:
                raise InvalidCommand('Invalid configuration parameter: ' + key)


    def getActionChannel(self, action):
        act_channel = ''
        if action == 'bid':
            act_channel = self.channels['bid_channel'].chan_name
        elif 'auction' in action:
            act_channel = self.channels['auction_channel'].chan_name

        return act_channel
