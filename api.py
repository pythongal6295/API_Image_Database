from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
from playhouse.dataset import DataSet
import socialnetwork_model as snm
import main 
import os


class Home(Resource):
    '''
    asks for visitor to see one of the other pages when the visitor loads the home page
    '''
    def get(self):
        return jsonify('Please visit /users, /images, or /differences for data.')

class Users(Resource):
    '''
    lists all the user's details and their status information
    '''
    def get(self):
        #db_connect = DataSet('sqlite:///socialnetwork.db')
        with snm.DbConnectionManager() as database:
            user_query = database.connection['Users'].all()
            if user_query:
                status_query = database.connection['Status'].all()
                result = {'users': [i for i in user_query], 'status': [i for i in status_query]}
                return jsonify(result)
            else:
                return jsonify('There is no data to show.')

class Images(Resource):
    '''
    Lists all users and their image information
    '''
    def get(self):
        with snm.DbConnectionManager() as database:
            image_query = database.connection['Picture'].all()
            if image_query:
                result = {'images': [i for i in image_query]}
                return jsonify(result)
            else:
                return jsonify('There is no data to show.')

class Differences(Resource):
    '''
    Lists all the files that are not in the database or on the disk
    '''
    def get(self):
        image_diff_dict = {}
        with snm.DbConnectionManager() as database:
            #I am not sure why the Picture table was not deleting the test user_id used in
            #socialnetwork_model to create the columns. Deleting it here.
            if database.connection['Picture']:
                database.connection['Picture'].delete(user_id='test')
                image_query = database.connection['Picture'].all()
                for i in image_query:
                    user_id = i['user_id']
                    file_tple = main.list_user_images(user_id, my_basedir)
                    image_diff_lsts = main.reconcile_images(user_id, file_tple, database.connection['Picture'])
                    image_diff_dict[user_id] = ((f'Images not saved in the database: {image_diff_lsts[0]}'), 
                        (f'Images not saved on disk: {image_diff_lsts[1]}'))
                result = image_diff_dict
                return jsonify(result)
            else:
                return jsonify ('There is no data to show.')


if __name__ == '__main__':

    my_basedir = os.path.curdir
    #my_basedir = 'C:\\Users\\kelly_kjenkz1\\UW_Python_320A\\Lesson_10\\assignment-10-pythongal6295'

    db_connect = DataSet('sqlite:///socialnetwork.db')

    app = Flask(__name__)

    api = Api(app)
    api.add_resource(Home, '/')
    api.add_resource(Users, '/users')
    api.add_resource(Images, '/images')
    api.add_resource(Differences, '/differences')

    app.run(port='5000')

    db_connect.close()