'''
Created on Feb 15, 2022

@author: JP
'''

from src.item import Item


class Bid(object):
    '''
    classdocs
    '''

    __action_list = {'Bid', 'End'}

    auction_id = 0
    bidder_id = 0
    action = "Bid"
    bid_value = 0
    notify = True
    auto_rebid = False
    auto_bid_amount = 0
    max_total_bids = 0

    def __init__(self):
        '''
        Default Constructor. Does nothing
        '''

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

    def addBid(self, *args, auction_item):
        if self.validate(auction_item):
            args

    def autoUpdateBid(self, last_bid):
        if self.auto_rebid and self.max_total_bids > 0:
            self.bid_value = last_bid + self.auto_bid_amount
            self.max_total_bids -= 1
            return True
        else:
            return False
