import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from db import db


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="this field cann't be left blank")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every Item needs a store_id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {
            "message": "item does not exist."
        }

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": 'The item already exists'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except Exception:
            return {
                "message": "An Error occurred during insertion to DataBase."
            }, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

            return {
                "message": "item has been deleted successfully."
            }

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        if ItemModel.find_by_name(name):
            try:
                item.save_to_db()
            except:
                return {
                    'message': "An Error has been occurred, UPDATE operation failed."
                }, 500
        else:
            try:
                item.save_to_db()
            except:
                return {
                    'message': "An Error has been occurred, INSERT operation failed."
                }, 500

        return item.json()


class Items_List(Resource):
    def get(self):
        return {
            "items": [item.json() for item in ItemModel.query.all()]
        }

        # list(map(lambda item: item.json(), ItemModel.query.all()))

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items"
        # query_output = cursor.execute(query)

        # results = {
        #     "items": []
        # }

        # if query_output:
        #     for row in query_output:
        #         # results['items'].append(ItemModel(*row).json())
        #         results['items'].append(ItemModel(row[1], row[2]).json())
        #     return results
        # else:
        #     return results
