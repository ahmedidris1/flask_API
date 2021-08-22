# import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from db import db

query_username = "SELECT * FROM users WHERE username = name"
query_user_id = "SELECT * FROM users WHERE id = id"


class UserRegister(Resource):
    __table__ = 'users'
    id = db.Column()
    username = db.Column()
    password = db.Column()
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username must be entered")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password must be entered")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {
                "message": f'A user with the name you have entered, does already exist'
            }, 400

        # user = UserModel(data['username'], data['password'])
        user = UserModel(**data)
        user.save_to_db()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data['username'], data['password']))

        # connection.commit()
        # connection.close()

        return {
            "message": "user created successfully."
        }, 201
