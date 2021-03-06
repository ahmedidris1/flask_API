from os import environ
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items_List
from resources.store import Store, Stores_list
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'DATABASE_URL',
    'sqlite:///data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ahmed'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items_List, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores_list, '/stores')


if __name__ == '__main__':
    db.init_app(app)
    port = environ.get('port', 5000)
    app.run(host="0.0.0.0", port=5000, debug=True)
