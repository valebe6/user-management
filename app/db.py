from pymongo import MongoClient
from flask import current_app, g

def get_db():
    if "db" not in g:
        client = MongoClient(current_app.config["MONGO_URI"])
        g.db_client = client
        g.db = client.get_default_database()
    return g.db

def close_db(e=None):
    client = g.pop("db_client", None)
    if client is not None:
        client.close()

class Mongo:
    def init_app(self, app):
        app.teardown_appcontext(close_db)

mongo = Mongo()
