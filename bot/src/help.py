'''
Created on Feb 19, 2022

@author: JP
'''


class Help(object):
    '''
    classdocs
    '''


    def printHelp(self, args):
        help_msg = 'The AutoAution bot supports the following commands:\n'\
            +'  creation_auction: Creates and publishes an auction with the provided inputs\n'\
            +'  edit_auction: Provides the ability for the seller to modify aspects of a currently active auction\n'\
            +'  bid: Adds an initial bid to an auction or updates an auction with a new bid\n'\
            +'  config: Configures the server specific auction channel names'\
            +'  help: Displays this message\n\n'\
            +'To see additional help on specific commands enter the command: !auction help command\n'\
            +'Example: !auction help create_auction'
        # A specific help command is given
        if len(args) == 1:
            if 'create_auction' == args[0]:
                help_msg = 'The create_auction has the following input parameters, order not restricted, any parameter inside [ ] are optional. Command:\n'\
                    +'!auction create_auction -item_name=item name [-item_desc=item description] [-quantity=number] -rarity=rarity '\
                        +' [-consumable=True/False] -end_date=YYYY/MM/DD HH:MM [-min_bid_inc=number]\n'\
                    +'Field details:\n'\
                    +'-item_name=str: The name of the item to be auctioned. Quotes are not needed.\n'\
                    +'-item_desc=str: Optional field containing a short description of the item being auctioned. Quotes are not needed.\n'\
                    +'-quantity=#: Optional field specifying the number of the same item being auctioned. Defaults to 1 if not specified.\n'\
                    +'-rarity=[Common,Uncommon,Rare,Very Rare,Legendary]: The rarity of the item being auction. Field restricted.\n'\
                    +'-consumable=[True/False,Yes/No]: Optional Field. Is the item being auctioned a consumable? Field restricted to'\
                        +' boolean terms. Defaults to False.\n'\
                    +'-end_date=YYYY/MM/DD HH:MM: The end date and time for the auction entered as local timezone referenced.'\
                        +' Field restricted to exact format.\n'\
                    +'-min_bid_inc=#: Optional field to specify the minimum bid increased after initial bid. Defaults to 1.'
            elif 'edit_auction' == args[0]:
                help_msg = 'The edit_auction has the following input parameters, order not restricted, all parameters are optional except for auction_id.'\
                        +' The auction is only updated for the specified fields, all other fields are unmodified.\n'\
                        +' Note: Only the seller can modify their own auction. Command:\n'\
                    +'!auction edit_auction -auction_id=# -item_name=item name -item_desc=item description -quantity=#'\
                        +' -rarity=rarity -consumable=True/False -end_date=YYYY/MM/DD HH:MM -min_bid_inc=#\n'\
                    +'Field details:\n'\
                    +'-auction_id=#: The id of the auction as indicated on the auction post.\n'\
                    +'-item_name=str: The name of the item to be auctioned. Quotes are not needed.\n'\
                    +'-item_desc=str: Field containing a short description of the item being auctioned. Quotes are not needed.\n'\
                    +'-quantity=#: Specifying the number of the same item being auctioned. Defaults to 1 if not specified.\n'\
                    +'-rarity=[Common,Uncommon,Rare,Very Rare,Legendary]: The rarity of the item being auction. Field restricted.\n'\
                    +'-consumable=[True/False,Yes/No]: Is the item being auctioned a consumable? Field restricted to'\
                        +' boolean terms. Defaults to False.\n'\
                    +'-end_date=YYYY/MM/DD HH:MM: The end date and time for the auction entered as local timezone referenced.'\
                        +' Field restricted to exact format.\n'\
                    +'-min_bid_inc=#: Specify the minimum bid increased after initial bid. Defaults to 1.'
            elif 'bid' == args[0]:
                help_msg = 'The bid action will create a new bid for the buyer or update a previous bid and bid parameters for the buyer. '\
                    +' The bid action has the following input parameters, order not restricted, any parameters inside [ ] are optional. Command:\n'\
                    +'!auction bid -auction_id=# -bid_value=# [-notify=True/False] [-auto_rebid=True/False] [-auto_bid_amount=#] [-max_total_bid=#]\n'\
                    +'Field details:\n'\
                    +'-auction_id=#: The id of the auction as indicated on the auction post.\n'\
                    +'-bid_value=#: The bid to be placed. The first bid must be the starting bid value. All subsequent bids must be the next valid bid,'\
                        +'which is equal to the current bid + minimum bid increment but not to exceed maximum bid increment as set by item rarity.'\
                        +' A bid value of 0 means that the bidder is exiting the auction and to be removed from list of bidders.\n'\
                    +'-notify=[True/False,Yes/No]: Optional field to have the bidder notified when they have been outbid on an item. Field restricted to'\
                        +' boolean terms. Defaults to True.\n'\
                    +'-auto_rebid=[True/False,Yes/No]: Optional field to automatically rebid on an item if outbid. Required if specifying auto_bid_amount'\
                        +' or max_total_bids fields. Field value retained on subsequent bid commands. Field restricted to boolean terms. Defaults to False.\n'\
                    +'-auto_bid_amount=#: Optional field to specify by how much to automatically increment the last bid on an auction item if was out bid.'\
                        +' Only valid if the auto_rebid field is specified as True or is currently not set to False.\n'\
                    +'-max_total_bid=#: Optional field to specify at what bid value automatically rebidding will stop if outbid on the auctionitem.'\
                        +' Only valid if the auto_rebid field is specified as True or is currently not set to False.\n'
            elif 'config' == args[0]:
                help_msg = 'Set the auction channel names for the server. The channels will need to be created prior to calling this command.'\
                        +' All parameters are optional. Command:\n'\
                    +'!auction config -auction_channel=name-of-channel -bid_channel=name-of-channel -chat_channel=name-of-channel'\
                        +' -trade_channel=name-of-channel -purge_auction=True/False -bidder_overwrite=True/False\n'\
                    +'Field details:\n'\
                    +'-auction_channel=name-of-channel: The name of the channel where sellers can enter commands to create/edit auctions and'\
                        +' where auctions will be posted by the bot.\n'\
                    +'-bid_channel=name-of-channel: The name of the channel where bidders can enter commands to bid on auctions and'\
                        +' where the bot will post the resolved bid command.\n'\
                    +'-chat_channel=name-of-channel: The name of the channel were auction related announcements are posted by the bot.\n'\
                    +'-trade_channel=name-of-channel: The name of the channel were completed auctions are posted by the bot.\n'\
                    +'-purge_auction=[True/False,Yes/No]: Should the auction and all associated bids be deleted from the database when the'\
                        +' auction is over? Field restricted to boolean terms. Defaults to False\n'\
                    +'-bidder_overwrite=[True/False,Yes/No]: Should only the last bid be kept for each bidder? Field restricted to boolean terms.'\
                        +' Defaults to False.\n'

        return help_msg
