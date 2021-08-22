from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items',
                        type=list,
                        required=True,
                        help="at least an empty list required")

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {
                "message": "store not found"
            }, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {
                "message": "this store already exists"
            }

        store = StoreModel(name)

        try:
            StoreModel.save_to_db(store)
        except:
            return {
                "message": "An Error occurred, insertion proccess failed."
            }, 500

        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {
                "message": "this store doen not exist"
            }
        else:
            store.delete_from_db()

        return {
            "message": "store has been deleted."
        }


class Stores_list(Resource):
    def get(self):
        return {
            "stores": [store.json() for store in StoreModel.query.all()]
        }
