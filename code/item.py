
import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


# this class inherits form the resource
class Item(Resource):
    # show filters of what to pass in and validation of what is expected
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        # return match name item in the list else returns None
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # for item in items:
        #     if item['name'] == name:
        #         return item

        # 200 is items exist else 404
        # return {'item': item}, 200 if item else 404

        # Get items from database
        item = self.find_by_name(name)

        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))

        # return result of the rows.
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):

        # if item return None item already exists else you can add the name
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': "An item with name '{}' already exists.".format(name)}, 404

        if self.find_by_name(name):
            # 404 Request cannot be fulfilled due to bad request
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        # data = request.get_json()

        item = {'name': name, 'price': data['price']}

        # # adding to list
        # items.append(item)

        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item, 201

    @classmethod
    def insert(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        # global items

        # #filtered element that dint much the name
        # items = list(filter(lambda x: x['name'] != name, items))

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()

        # data = request.get_json()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        # item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500
        return updated_item

    @classmethod
    def update(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return {'items': items}
