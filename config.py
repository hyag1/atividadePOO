import os

class Config(object):
    CSRF_ENABLE= True
    SECRET = '2cbe13972c4067ebee6437e9bf8b0efa1d869357b4289c3b1b830bd2f602afcd'
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
    ROOT_DIR=os.path.dirname(os.path.abspath(__file__))
    APP = None
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/minisigaa.db'


class DevelopmentConfig(Config):
    TESTING= True
    DEBUG=True
    IP_HOST='localhost'
    PORT_HOST = 8000
    URL_MAIN= 'http://%s/%s' % (IP_HOST,PORT_HOST)

app_config={
    'development': DevelopmentConfig(),
    'testing': None,
    'production': None
}

app_active=os.getenv('FLASK_ENV')

if app_active is None:
    app_active='development'


