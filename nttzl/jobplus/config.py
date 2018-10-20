class BaseConfig(object):
    TEMPLATES_AUTO_RELOAD=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY='\xf1\x9e\x96\x1e\xf2\x82A\x11\xd9%\x99?\x9bP\xb3\x0f,\xd6\xd5\xeb\xc2\xb6\xd6\x1b'
    INDEX_PER_PAGE = 9
    ADMIN_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
        DEBUG=True
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

configs = {
        'development':DevelopmentConfig,
        'production':ProductionConfig,
        'testing':TestingConfig
        }

