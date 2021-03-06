import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from flask_cors import CORS
from datetime import timedelta

from security import authenticate, identity
from resources.user import UserRegister, User
from resources.bill import Bill, BillList, LatestBill
from resources.bill_category import BillCategory, BillCategoryList
from resources.task import Task, TaskList, MyTasks

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # turns off flask_sqlalchemy modification tracker
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'bart'

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

# TODO usun przed wrzuceniem na heroku
# @app.before_first_request
# def create_tables():
#     db.create_all()


jwt = JWT(app, authenticate, identity)  # creates /auth endpoint

app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)     # change later

api.add_resource(BillCategory, '/bill_category/<string:name>')
api.add_resource(Bill, '/bill', '/bill/<int:bill_id>')
api.add_resource(BillList, '/bills')
api.add_resource(BillCategoryList, '/bill_categories')
api.add_resource(LatestBill, '/latest_bill')
api.add_resource(Task, '/task', '/task/<int:task_id>')
api.add_resource(TaskList, '/tasks')
api.add_resource(MyTasks, '/my_tasks')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user', '/user/<int:user_id>')

# if it's not __main__, it means we have imported this file (don't run the app then)
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)