'''
Created on Feb 15, 2022

@author: JP
'''

import re
from src.database import AHDatabase
from src.item import Item
from src.utils import ParseArgs, InvalidCommand


class Bid(object):
    '''
    classdocs
    '''

    auction_id = 0
    bidder_name = ""
    bid_id = 0
    bid_value = 0
    notify = True
    auto_rebid = False
    auto_bid_amount = 0
    max_total_bids = 0


    def __init__(self, in_dict = {}):
        '''
        Default Constructor. Does nothing
        '''
        if len(in_dict) > 0:
            for k, v in in_dict.items():
                setattr(self, k, v)
        else:
            self.auction_id = 0
            self.bidder_name = ""
            self.bid_id = 0
            self.bid_value = 0
            self.notify = True
            self.auto_rebid = False
            self.auto_bid_amount = 0
            self.max_total_bids = 0


    def validate(self, auction_item = Item):
        '''
        Validates the inputs for the new bid. If any of the bid parameters are incorrect,
        '''
        global __action_list
        msg = ""

        if self.action not in self.__action_list:
            msg = "Invalid Bid command entered: " + self.action
        if self.bid_value < auction_item.getMinBid():
            msg += "\nInvalid bid value, below bid minimum: " + str(auction_item.getMinBid())
        if self.bid_value > 2 * auction_item.getMinBid():
            msg += "\nInvalid bid value, above bid maximum: " + str(2 * auction_item.getMinBid())
        if self.auto_rebid == True:
            if self.auto_bid_amount < auction_item.getMinBid():
                msg += "\nInvalid auto re-bid value, below bid minimum: " + str(auction_item.getMinBid())
            if self.auto_bid_amount > auction_item.getMinBid():
                msg += "\nInvalid auto re-bid value, above bid maximum: " + str(2 * auction_item.getMinBid())
            if self.max_total_bids < 1:
                msg += "\nInvalid maximum total number of automatic rebids, must be 1 or greater"

        if msg:
            print(msg)


    @staticmethod
    def addBid(b_cmd, args, guild_id):
        db = AHDatabase()
        act_args = ParseArgs.tupleToDict(args)
        try:
            auction_id = act_args['auction_id']
        except:
            raise InvalidCommand('The auction_id argument is missing from command')
        auction_record = db.getAuctionRecord(guild_id, auction_id)
        if auction_record.auction_id == -1:
            raise InvalidCommand('The requested auction does not exist. Auction_id: ' + auction_id)

        ah_post = b_cmd.channel.fetch_message(auction_record.message_id)
        bid = Bid(db.getBidRecord(guild_id, auction_record, str(b_cmd.author)))
        if bid.bid_id == -1:
            bid = Bid(act_args)
            bid.bid_id = db.getNextBidID()
            bid.bidder_name = str(b_cmd.author)

        bid_upd = ah_post.content
        bid_upd = re.sub(r'(.*Current bid: ).+(\n.*)', r'\1' + b_cmd.author.mention + ' ' + str(bid.bid_value) + r'gp\2', bid_upd)

        if bid.validate(auction_record):
            db.addBidRecord(guild_id, vars(bid))
            return ah_post, bid_upd


    def autoUpdateBid(self, last_bid):
        if self.auto_rebid and self.max_total_bids > 0:
            self.bid_value = last_bid + self.auto_bid_amount
            self.max_total_bids -= 1
            return True
        else:
            return False
