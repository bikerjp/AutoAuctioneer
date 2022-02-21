'''
Created on Feb 19, 2022

@author: JP
'''


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
        if '-' in temp and '=' in temp:
            for param in temp.split('-'):
                param = param.strip()
                if param:
                    k, v = param.split('=')
                    arg_dict[k] = v.strip()

        return arg_dict


    @staticmethod
    def removeCommand(tup):
        new_tup = tup[1:]

        return (new_tup)
