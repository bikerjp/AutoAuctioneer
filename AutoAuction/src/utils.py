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
    def tupleToDict(p_tup):
        temp = ' ' + ' '.join(p_tup)
        arg_dict = None
        if '-' in temp and ':' in temp:
            for param in temp.split('-'):
                param = param.strip()
                if param:
                    k, v = param.split(':')
                    arg_dict[k] = v.strip()

        return arg_dict
