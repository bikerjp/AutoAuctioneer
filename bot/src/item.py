'''
Created on Feb 15, 2022

@author: JP
'''

from datetime import datetime
from datetime import timezone
from datetime import timedelta
import re
import distutils.util
from src.database import AHDatabase
from src.utils import InvalidCommand
from src.utils import ParseArgs


class Item(object):
    '''
    classdocs
    '''
    __bid_mins = {'Common': 25, 'Uncommon': 100, 'Rare': 700, 'Very Rare': 7000, 'Legendary': 25000}
    auctioneer = ""
    message_id = 0
    auction_id = 0
    item_name = ""
    item_desc = ""
    rarity = ""
    consumable = False
    quantity = 1
    end_date = datetime.now()
    min_bid_inc = 1
    time_extended = False


    def __init__(self, in_dict = {}):
        '''
        Constructor
        '''
        if len(in_dict) > 0:
            for k, v in in_dict.items():
                if k != 'end_date':
                    setattr(self, k, v)
                else:
                    # for local database testing no transform needed
                    self.end_date = v
#                    self.end_date = datetime.fromisoformat(v)
        else:
            self.auctioneer = ""
            self.message_id = 0
            self.auction_id = 0
            self.item_name = ""
            self.item_desc = ""
            self.rarity = ""
            self.consumable = False
            self.quantity = 1
            self.end_date = datetime.now().astimezone(tz = timezone.utc)
            self.min_bid_inc = 1
            self.time_extended = False


    def validArgs(self):
        if not self.item_name:
            raise InvalidCommand('Item name cannot be an empty string')
        if self.rarity not in self.__bid_mins.keys():
            raise InvalidCommand('Invalid item rarity: ' + self.rarity + '. Item rarity must be one of: ' + self.__bid_mins.keys())
        if self.quantity < 1:
            raise InvalidCommand('Invalid quantity given: ' + str(self.quantity) + '. Must be a positive number 1 or greater')
        if self.min_bid_inc < 1 or self.min_bid_inc > (self.__bid_mins[self.rarity] / 2):
            raise InvalidCommand('Invalid argument for min_bid: ' + str(self.min_bid_inc) + \
                                 '. Must be a positive number 1 or greater and less-than or equal to half item value. Enterd: '\
                                 +str(self.min_bid_inc))


    def getMinBid(self):
        return self.__bid_mins[self.rarity] if not self.consumable else self.__bid_mins[self.rarity] / 2


    def createAuction(self, author, args):
        db = AHDatabase()
        if not self.auctioneer:
            self.auctioneer = author
        if len(args) == 1:
            raise InvalidCommand('No arguments provided.')
        arg_dict = ParseArgs.tupleToDict(args)
        try:
            self.item_name = arg_dict['item_name']
            if 'item_desc' in arg_dict.keys():
                self.item_desc = arg_dict['item_desc']
            self.rarity = arg_dict['rarity']
            try:
                self.consumable = distutils.util.strtobool(arg_dict['consumable'])
            except ValueError as err:
                raise InvalidCommand('Invalid argument for consumable: ' + str(err) + '. Must be a true/false or yes/no, case insensitive.')
            if 'quantity' in arg_dict.keys():
                self.quantity = int(arg_dict['quantity'])
            try:
                self.end_date = datetime.strptime(arg_dict['end_date'], '%Y/%m/%d %H:%M').replace(tzinfo = None).astimezone(tz = timezone.utc)
            except Exception as err:
                raise InvalidCommand('Invalid date time entered:' + str(err))
            if 'min_bid_inc' in arg_dict.keys():
                self.min_bid_inc = int(arg_dict['min_bid_inc'])
        except Exception as err:
            raise InvalidCommand('Unable to create auction due to error: ' + str(err))

        self.validArgs()

        self.auction_id = db.getNextAuctionID()


    def extendTime(self, post_content) -> str:
        if not self.time_extended:
            self.time_extended = True
            self.end_date = self.end_date + timedelta(hours = 12)
            post_content = re.sub(r'(.*Ending date and time \(UTC\)): [0-9:\-\+ ]+(\n.*)', r'\1 - Extended to: ' + str(self.end_date) + r'\2', post_content)
        return post_content


    @staticmethod
    async def editAuction(guild_id, msg_channel, args) -> str:
        db = AHDatabase()
        arg_dict = ParseArgs.tupleToDict(args)

        try:
            auction_id = arg_dict['auction_id']
        except:
            raise InvalidCommand('Missing required parameter: -auction_id=<value>')

        record = Item(db.getAuctionRecord(guild_id, auction_id))

        ah_post = msg_channel.fetch_message(record.message_id)
        post_content = ah_post.content

        if 'item_name' in arg_dict.keys():
            record.item_name = arg_dict['item_name']
            post_content = re.sub(r'(.*Auctioning: ).+(\n.*)', r'\1' + record.item_name + r'\2', post_content)
        if 'item_desc' in arg_dict.keys():
            record.item_desc = arg_dict['item_desc']
            post_content = re.sub(r'(.*Description: ).*(\n\n.*)', r'\1' + record.item_desc.replace('\\n', '\n') + r'\2', post_content)
        if 'rarity' in arg_dict.keys():
            record.rarity = arg_dict['rarity']
            post_content = re.sub(r'(.*Starting bid: ).+(\n.*)', r'\1' \
                +str(record.__bid_mins[record.rarity] if not record.consumable else record.__bid_mins[record.rarity] / 2) + 'gp\n' \
                +r'\2', post_content)
        if 'consumable' in arg_dict.keys():
            try:
                record.consumable = distutils.util.strtobool(arg_dict['consumable'])
            except ValueError as err:
                raise InvalidCommand('Invalid argument for consumable: ' + str(err) + '. Must be a true/false or yes/no, case insensitive.')
            post_content = re.sub(r'(.*Starting bid: ).+(\n.*)', r'\1' \
                +str(record.__bid_mins[record.rarity] if not record.consumable else record.__bid_mins[record.rarity] / 2) + r'gp\2', post_content)
        if 'quantity' in arg_dict.keys():
            record.quantity = int(arg_dict['quantity'])
            post_content = re.sub(r'(.*Quantity: ).+(\n.*)', r'\1' + record.item_desc + r'\2', post_content)
        if 'end_date' in arg_dict.keys():
            try:
                record.end_date = datetime.strptime(arg_dict['end_date'], '%Y/%m/%d %H:%M').replace(tzinfo = None).astimezone(tz = timezone.utc)
                post_content = re.sub(r'(.*Ending date and time \(UTC\): )[0-9:\-\+ ]+(\n.*)', r'\1' + str(record.end_date) + r'\2', post_content)
            except Exception as err:
                raise InvalidCommand('Invalid argument for end date and time. Enter in isoformat "YYYY/MM/DD HH:MM". Entered time: ' + str(err))
        if 'min_bid_inc' in arg_dict.keys():
            record.min_bid_inc = int(arg_dict['min_bid_inc'])
            post_content = re.sub(r'(.*Bid increments: ).*(\n.*)', r'\1' + str(record.min_bid_inc) + 'gp - ' \
                +str(record.__bid_mins[record.rarity] * 2 if not record.consumable else record.__bid_mins[record.rarity]) + 'gp\2'\
                , post_content)

        record.validArgs()

        return ah_post, post_content


    def createPost(self, p_guild) -> str:
        ah_str = "Seller: " + p_guild.get_member_named(self.auctioneer).mention + "\n"\
            +"Auction id: " + str(self.auction_id) + "\n"\
            +"Auctioning: " + self.item_name + "\n"\
            +"Description: " + self.item_desc.replace('\\n', '\n') + "\n\n"\
            +"Quantity: " + str(self.quantity) + "\n\n"\
            +"Starting bid: " + str(self.__bid_mins[self.rarity] if not self.consumable else self.__bid_mins[self.rarity] / 2) + "gp\n"\
            +"Current bid: \n"\
            +"Bid increments: " + str(self.min_bid_inc) + "gp - "\
                +str(self.__bid_mins[self.rarity] * 2 if not self.consumable else self.__bid_mins[self.rarity]) + "gp\n\n"\
            +"Ending date and time (UTC): " + str(self.end_date) + "\n\n"\
            +"Click the 🕰 reaction️ to receive a message with Auction end date and time converted to your local time zone\n"\
            +"Only the auction creator can react to the 🛑 reaction."

        return ah_str
