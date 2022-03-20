'''
Creates DB tables for the social network model
'''

import os
from loguru import logger
from playhouse.dataset import DataSet

#pylint: disable=R0903, C0103


class DbConnectionManager():
    '''context manager for the sql database connection'''
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = DataSet('sqlite:///socialnetwork.db')
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()



def users_columns(users_table):
    '''
    Creates unique columns for the Users DB table
    '''
    users_table.insert(user_id='test')
    users_table.create_index(['user_id'], unique=True)
    users_table.delete(user_id='test')

    users_table.insert(user_name='test')
    users_table.create_index(['user_name'])
    users_table.delete(user_name='test')

    users_table.insert(user_last_name='test')
    users_table.create_index(['user_last_name'])
    users_table.delete(user_last_name='test')

    users_table.insert(user_email='test')
    users_table.create_index(['user_email'])
    users_table.delete(user_email='test')


def status_columns(status_table):
    '''
    Creates unique columns for the Status DB table
    '''
    status_table.insert(status_id='test')
    status_table.create_index(['status_id'], unique=True)
    status_table.delete(status_id='test')

    status_table.insert(user_id='test')
    status_table.create_index(['user_id'])
    status_table.delete(user_id='test')

    status_table.insert(status_text='test')
    status_table.create_index(['status_text'])
    status_table.delete(status_text='test')


def picture_columns(picture_table):
    '''
    Creates unique columns for the Picture DB table
    '''

    picture_table.insert(picture_id='test')
    picture_table.create_index(['picture_id'], unique=True)
    picture_table.delete(picture_id='test')
    #del picture_table[1]

    picture_table.insert(user_id='test')
    picture_table.create_index(['user_id'])
    picture_table.delete(picture_id='test')
    #del picture_table[1]

    picture_table.insert(tags='test')
    picture_table.create_index(['tags'])
    picture_table.delete(tags='test')
    #del picture_table[1]

