from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from security import authenticate, identify

from user import UserRegister

# import item and itemList form item
from item import Item, ItemList

app = Flask(__name__)
# assihng app  to the api
api = Api(app)

app.secret_key = '54321'

# list that will hold the dictinaries

jwt = JWT(app, authenticate, identify)  # creates a new endpoint know us /auth
items = []


# http://127.0.0.1:5000/student/ian
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
