'''
Created on Feb 19, 2022

@author: JP
'''

import re


class InvalidCommand(Exception):
    '''
    Derived Exception object for all invalid commands or arguments containing the error message to be sent to the user
    '''
    pass


class ParseArgs(object):
    '''
    Utilty class to convert a tuple to the a dictionary
    '''


    @staticmethod
    def tupleToDict(tup):
        temp = '' + ' '.join(tup)
        arg_dict = dict()
        while temp:
            str_match = re.match(r'-([a-z0-9_]+)=(.*?)[ ]*(-[a-z0-9_]+=.*$)', temp)
            if str_match is not None:
                arg_dict[str_match.group(1)] = str_match.group(2)
                # Check to see if there are any more parameters to be parsed
                if len(str_match.groups()) == 3:
                    temp = str_match.group(3)
                else:
                    temp = ''
            else:
                # check to see if last parameter in string
                str_match = re.match(r'-([a-z0-9_]+)=(.*)', temp)
                if str_match is not None:
                    arg_dict[str_match.group(1)] = str_match.group(2)
                temp = ''

        return arg_dict


    @staticmethod
    def removeCommand(tup):
        new_tup = tup[1:]

        return (new_tup)
