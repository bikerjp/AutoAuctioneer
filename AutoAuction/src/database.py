'''
Created on Feb 15, 2022

@author: JP
'''
import mysql.connector
from src.item import Item
from discord import guild
from src.configuration import Configuration
from src.utils import InvalidCommand


class AHDatabase(object):
    '''
    classdocs
    '''

    __conn = mysql.connector.connection.MySQLConnection

    def __init__(self):
        '''
        Constructor
        '''
        self.__conn = mysql.connector.connect(user = 'ah_bot', password = '', host = 'localhost', database = 'mysql')

    def addNewAuctionHouse(self, p_guild: guild):
        # create a new auction
        if self.__conn.is_connected():
            p_guild
        else:
            raise InvalidCommand("database:addNewAuctionHouse - Not connected to the database")

    def addAuctionRecord(self, guild_id, auction_item: Item):
        if self.__conn.is_connected():
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

    def closeAuction(self, guild_id, auction_id, cancelled = False):
        if self.__conn.is_connected():
            guild_id
            auction_id
            if cancelled:
                auction_id
        else:
            raise InvalidCommand("database:closeAuction - Not connected to the database")

    def closeConnection(self):
        if self.__conn.is_connected():
            self.__conn.close()
        else:
            raise InvalidCommand("database:closeConnection - Not connected to the database")

    def getAuctionRecord(self, guild_id, msg_id):
        #
        record = None
        if self.__conn.is_connected():
            # get auction record by auction id
            record
            guild_id
            msg_id
        else:
            raise InvalidCommand("database:getAuctionRecord - Not connected to the database")

        return record

    def addBidRecord(self, guild_id, auction_id):
        record = None
        if self.__conn.is_connected():
            # get auction record by auction id
            record
            guild_id
            auction_id
        else:
            raise InvalidCommand("database:addBidRecord - Not connected to the database")

    def getBidRecord(self, guild_id, auction_id):
        record = None
        if self.__conn.is_connected():
            # get auction record by auction id
            record
            guild_id
            auction_id
        else:
            raise InvalidCommand("database:getBidRecord - Not connected to the database")

    def getNextAuctionID(self):
        next_id = -1
        if self.__conn.is_connected():
            return next_id
        else:
            raise InvalidCommand("database:getNextAuctionId - Not connected to the database")

    def getNextBidID(self):
        next_id = -1
        if self.__conn.is_connected():
            return next_id
        else:
            raise InvalidCommand("database:getNextBidId - Not connected to the database")

    def addConfigFile(self, guild_id, ah_config):
        if self.__conn.is_connected():
            guild_id
            ah_config
            # get configuration table from datase for the guild
            # populate config object
        else:
            raise InvalidCommand("database:addConfigFile - Not connected to the database")

    def getConfigFile(self, guild_id) -> Configuration:
        if self.__conn.is_connected():
            guild_id
            config = Configuration()
            # get configuration table from datase for the guild
            # populate config object
            return config
        else:
            raise InvalidCommand("database:getConfigFile - Not connected to the database")
