'''
Created on Feb 15, 2022

@author: JP
'''

import copy
import mysql.connector
from discord import guild
from src.utils import InvalidCommand
from src.singleton import Singleton


class Auctions():
    fields = {}
    bids = {}


    def __init__(self):
        self.fields = {}
        self.bids = {}


class AHDatabase(metaclass = Singleton):
    '''
    classdocs
    '''

    __conn = None


    class Guilds():
        auctions = {}
        config = {}


        def __init__(self):
            self.auctions = {}
            self.config = {}


    __guilds = {}

    __next_auction_id = 1
    __next_bid_id = 1


    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''

        # temporary username and password
        if self.__conn is None:
            self.__conn = mysql.connector.connect(user = 'user', password = 'some_pass_word', host = 'localhost', database = 'mysql')


    def addNewAuctionHouse(self, p_guild: guild):
        # create a new auction
        if self.isConnected():
            guild = self.Guilds()
            self.__guilds[p_guild.id] = guild
        else:
            raise InvalidCommand("database:addNewAuctionHouse - Not connected to the database")


    def isConnected(self):
        if self.__conn is not None and self.__conn.is_connected():
            return True
        else:
            return False


    def addAuctionRecord(self, guild_id, auction_item):
        if self.isConnected():
            auction = Auctions()
            auction_id = auction_item['auction_id']
            # check to see if the auction id already exists to keep all recorded bids
            if auction_id in self.__guilds[guild_id].auctions:
                auction = self.__guilds[guild_id].auctions[auction_id]
            auction.fields = auction_item
            self.__guilds[guild_id].auctions[auction_id] = auction
        else:
            raise InvalidCommand("database:addAuctionRecord - Not connected to the database")


    def closeAuction(self, guild_id, auction_id):
        if self.isConnected():
            try:
                self.__guilds[guild_id].auctions.pop(auction_id)
                cancelled = False
            except:
                raise InvalidCommand('Auction id (' + str(auction_id) + ') could not be found')
            return cancelled
        else:
            raise InvalidCommand("database:closeAuction - Not connected to the database")


    def closeConnection(self):
        if self.isConnected():
            self.__conn.close()
        else:
            raise InvalidCommand("database:closeConnection - Not connected to the database")


    def getAuctionRecord(self, guild_id, auction_id):
        #
        if self.isConnected():
            if auction_id in self.__guilds[guild_id].auctions:
                return self.__guilds[guild_id].auctions[auction_id].fields
            else:
                # no auction record found, return an empty dictionary
                return {}
        else:
            raise InvalidCommand("database:getAuctionRecord - Not connected to the database")


    def addBidRecord(self, guild_id, auction_id, bid):
        if self.isConnected():
            # check to see if the auction id already exists to keep all recorded bids
            if auction_id in self.__guilds[guild_id].auctions:
                # get auction record by auction id
                auction = self.__guilds[guild_id].auctions[auction_id]
                auction.bids[bid['bidder_name']] = bid
                self.__guilds[guild_id].auctions[auction_id] = auction
            else:
                raise InvalidCommand('Unable to add bid for auction id(' + str(auction_id) + ') - auction does not exist')
        else:
            raise InvalidCommand("database:addBidRecord - Not connected to the database")


    def getBidRecord(self, guild_id, auction_id, bidder_name):
        if self.isConnected():
            try:
                return self.__guilds[guild_id].auctions[auction_id].bids[bidder_name]
            except:
                # No bid record found for bidder, return empty dictionary
                return {}
        else:
            raise InvalidCommand("database:getBidRecord - Not connected to the database")


    def getNextAuctionID(self):
        if self.isConnected():
            next_id = self.__next_auction_id
            self.__next_auction_id += 1
            return next_id
        else:
            raise InvalidCommand("database:getNextAuctionId - Not connected to the database")


    def getNextBidID(self):
        if self.isConnected():
            next_id = self.__next_bid_id
            self.__next_bid_id += 1
            return next_id
        else:
            raise InvalidCommand("database:getNextBidId - Not connected to the database")


    def addConfigFile(self, guild_id, ah_config):
        if self.isConnected():
            self.__guilds[guild_id].config = copy.deepcopy(ah_config)
            # get configuration table from datase for the guild
            # populate config object
        else:
            raise InvalidCommand("database:addConfigFile - Not connected to the database")


    def getConfigFile(self, guild_id):
        if self.isConnected():
            try:
                return self.__guilds[guild_id].config
            except:
                # no config record found, return an empty dictionary
                return {'':{}}
        else:
            raise InvalidCommand("database:getConfigFile - Not connected to the database")
