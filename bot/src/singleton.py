'''
Created on Feb 21, 2022

@author: JP
'''


class Singleton(type):
    '''
    classdocs
    '''
    _instances = {}


    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

