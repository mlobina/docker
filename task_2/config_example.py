class Configuration(object):
    DEBUG = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRE_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/adv_db'

