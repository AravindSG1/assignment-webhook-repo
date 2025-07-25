from flask import Flask

from app.webhook.routes import webhook
from app.extensions import mongo

# Creating our flask app
def create_app():

    app = Flask(__name__)

    # Add MongoDB URI here
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_webhook_db"

    # Initialize Mongo
    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
