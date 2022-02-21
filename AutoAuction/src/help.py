'''
Created on Feb 19, 2022

@author: JP
'''

valid_cmds = ['create_auction', 'edit_auction', 'cancel_auction', 'bid', 'config', 'help']


class Help(object):
    '''
    classdocs
    '''

    def printHelp(self, *args):
        help_msg = ''
        arg = ''.join(args)
        if not args:
            # populate the high level help message
            help_msg = 'The'
        elif 'create_auction' == arg:
            help_msg
        elif 'edit_auction' == arg:
            help_msg
        elif 'cancel_auction' == arg:
            help_msg
        elif 'bid' == arg:
            help_msg
        elif 'config' == arg:
            help_msg
        else:
            help_msg

        return help_msg
