'''
Created on Feb 15, 2022

@author: JP
'''

import distutils.util
import re
from src.configuration import Configuration
from src.database import AHDatabase
from src.item import Item
from src.utils import InvalidCommand


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
    max_total_bid = 0
    cancel = False


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
            self.max_total_bid = 0
            self.cancel = False


    def validate(self, first, auction_item, curr_bid):
        '''
        Validates the inputs for the new bid. If any of the bid parameters are incorrect,
        '''
        global __action_list
        msg = ""

        if first:
            if self.bid_value != auction_item.getMinBid():
                msg += "\n - Invalid bid value (" + str(self.bid_value) + ") does not equal initial bid: " + str(auction_item.getMinBid())
        else:
            if self.bid_value < curr_bid + auction_item.min_bid_inc:
                msg += '\n - Invalid bid value. (' + str(self.bid_value) + ') must be greater than ' + \
                                      str(curr_bid + auction_item.min_bid_inc)
            if self.bid_value > curr_bid + (2 * auction_item.getMinBid()):
                msg += "\n - Invalid bid value, above maximum bid increment: " + str(curr_bid + (2 * auction_item.getMinBid()))

        if self.auto_rebid:
            if self.auto_bid_amount < auction_item.min_bid_inc:
                msg += "\n - Invalid auto re-bid value (" + str(self.auto_bid_amount) + "), below minimum bid increment: "\
                    +str(auction_item.min_bid_inc)
            if self.auto_bid_amount > auction_item.getMinBid():
                msg += "\n - Invalid auto re-bid value (" + str(self.auto_bid_amount) + "), above maximum bid increment: "\
                    +str(2 * auction_item.getMinBid())
            if self.max_total_bid < auction_item.getMinBid():
                msg += "\n - Invalid maximum automatic rebid value(" + str(self.max_total_bid) + "), must be greater than the "\
                    +"minimum bid of " + str(auction_item.getMinBid())

            if msg:
                msg = "Auction item: " + auction_item.item_name + " - Bid issues:" + msg
                raise InvalidCommand(msg)

        return True


    @staticmethod
    def addBid(b_cmd, args, guild_id, auction_record, ah_post):
        db = AHDatabase()
        first = False
        curr_bid = 0

        bid = Bid(db.getBidRecord(guild_id, auction_record.auction_id, str(b_cmd.author)))
        try:
            bid.bid_value = float(args['bid_value'])
        except KeyError as err:
            raise InvalidCommand('Did not specify bid_value parameter and value. See !auction help bid for further details')
        except:
            raise InvalidCommand('Entered bid_value: ' + str(args['bid_value']) + ' is not a number.')

        if bid.bid_id == 0:
            bid.bid_id = db.getNextBidID()
            bid.bidder_name = str(b_cmd.author)
            bid.notify = True
            bid.auto_rebid = False
            first = True
        else:
            bid_match = re.search(r'.*Current bid:(.*\>) ([0-9.]*)gp\n.*', ah_post)
            if bid_match is not None:
                curr_bidder = bid_match.group(1)
                curr_bid = int(bid_match.group(2))

            if curr_bidder == bid.bidder_name:
                if bid.cancel:
                    return ah_post, '', bid.bidder_name, True
                else:
                   raise InvalidCommand('Already highest bidder')

        if 'auto_bid_amount' in args:
            bid.auto_bid_amount = int(args['auto_bid_amount'])
        if 'auto_rebid' in args:
            try:
                bid.auto_rebid = distutils.util.strtobool(args['auto_rebid'])
            except ValueError as err:
                raise InvalidCommand('Invalid argument for auto_rebid: ' + err + '. Must be a true/false or yes/no, case insensitive.')
        if 'max_total_bid' in args:
            bid.max_total_bids = int(args['max_total_bid'])
        if 'notify' in args:
            try:
                bid.notify = distutils.util.strtobool(args['notify'])
            except ValueError as err:
                raise InvalidCommand('Invalid argument for notify: ' + err + '. Must be a true/false or yes/no, case insensitive.')

        bid_upd = re.sub(r'(.*Current bid:).*(\n.*)', r'\1' + b_cmd.author.mention + ' ' + str(bid.bid_value) + r'gp\2', ah_post)
        bid_post = b_cmd.author.mention + ' is bidding ' + str(bid.bid_value) + 'gp on item ' + auction_record.item_name \
            + ' for auction id: ' + auction_record.auction_id

        if bid.validate(first, auction_record, curr_bid):
            db.addBidRecord(guild_id, auction_record.auction_id, vars(bid))
            return bid_upd, bid_post, bid.bidder_name, False


    @staticmethod
    def autoUpdateBid(guild_id, auction_record, ah_post):
        db = AHDatabase()
        bid_post = ''
        bid_upd = ah_post

        # returns a dictionary of all valid bis for the auction, indexed by
        bidders = db.getAuctionBidList(guild_id, auction_record.auction_id)

        return bid_upd, bid_post, bid.bidder_name
