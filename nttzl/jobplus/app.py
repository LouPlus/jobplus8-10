from flask import Flask, render_template
from .config import configs
from .models import db,User,Company,Job,Delivery

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)
    register_blueprints(app)

    return app

def register_blueprints(app):
    from .handlers import admin,user,front,company,job
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(front)
    app.register_blueprint(company)
    app.register_blueprint(job)



