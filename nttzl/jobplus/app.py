from flask import FLASK, render_template
from config import configs
from models import db,User,Company,Position

def create_app(config):
    app = FLASK(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)
    return app

