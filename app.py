# from flask import Flask
from api.v1 import create_app
# from db import db
# app = Flask(__name__)
api = create_app( True)

# db.init_app(app)
# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    api.run(debug=True)