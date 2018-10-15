class BaseConfig():
    TEMPLATES_AUTO_RELOAD=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY='make sure to make a secret key'

class DevelopmentConfig(BaseConfig):
        DEBUG=True
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

configs = {
        'development':DevelopmentConfig
        'production':ProductionConfig
        'testing':TestingConfig
        }

