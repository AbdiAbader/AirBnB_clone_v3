#!/usr/bin/python3


from flask import Flask
import app_views as views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(views.app_views)

if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)