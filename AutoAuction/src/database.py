'''
Created on Feb 15, 2022

@author: JP
'''
import mysql.connector
from discord import guild
from src.utils import InvalidCommand
from src.singleton import Singleton


class AHDatabase(metaclass = Singleton):
    '''
    classdocs
    '''

    __conn = None


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
            p_guild
        else:
            raise InvalidCommand("database:addNewAuctionHouse - Not connected to the database")


    def isConnected(self):
        if self.__conn is not None and self.__conn.is_connected():
            return True
        else:
            return False


    def addAuctionRecord(self, guild_id, auction_item):
        if self.isConnected():
            auction_item
            guild_id
        # if auction_item not in database
            # create new database record
            # get next available auction id
            # populate database record with auction_item
        # else
            # report error and return
        else:
            raise InvalidCommand("database:addAuctionRecord - Not connected to the database")


    def closeAuction(self, guild_id, auction_id):
        if self.isConnected():
            guild_id
            auction_id
        else:
            raise InvalidCommand("database:closeAuction - Not connected to the database")


    def closeConnection(self):
        if self.isConnected():
            self.__conn.close()
        else:
            raise InvalidCommand("database:closeConnection - Not connected to the database")


    def getAuctionRecord(self, guild_id, auction_id):
        #
        record = {}
        if self.isConnected():
            # get auction record by auction id
            record
            guild_id
            auction_id
        else:
            raise InvalidCommand("database:getAuctionRecord - Not connected to the database")

        return record


    def getAuctionRecordFromMsgId(self, guild_id, msg_id):
        #
        record = {}
        if self.isConnected():
            # get auction record by auction id
            record
            guild_id
            msg_id
        else:
            raise InvalidCommand("database:getAuctionRecord - Not connected to the database")

        return record


    def addBidRecord(self, guild_id, bid):
        record = {}
        if self.isConnected():
            # get auction record by auction id
            record
            guild_id
            bid
        else:
            raise InvalidCommand("database:addBidRecord - Not connected to the database")


    def getBidRecord(self, guild_id, auction_id, bidder):
        if self.isConnected():
            # get auction record by auction id
            record = None
            guild_id
            bidder
            auction_id
            # get all bids from the guild auction house for the specific auction id
            # loop through all bid records
                # if bidder name matches a bid record, retrieve bid record

            return record
        else:
            raise InvalidCommand("database:getBidRecord - Not connected to the database")


    def getNextAuctionID(self):
        next_id = -1
        if self.isConnected():
            return next_id
        else:
            raise InvalidCommand("database:getNextAuctionId - Not connected to the database")


    def getNextBidID(self):
        next_id = -1
        if self.isConnected():
            return next_id
        else:
            raise InvalidCommand("database:getNextBidId - Not connected to the database")


    def addConfigFile(self, guild_id, ah_config):
        if self.isConnected():
            guild_id
            ah_config
            # get configuration table from datase for the guild
            # populate config object
        else:
            raise InvalidCommand("database:addConfigFile - Not connected to the database")


    def getConfigFile(self, guild_id):
        if self.isConnected():
            guild_id
            config = {'':{}}
            # get configuration table from datase for the guild
            # populate config object
            return config
        else:
            raise InvalidCommand("database:getConfigFile - Not connected to the database")
