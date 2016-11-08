class Configuration(object):
    DATABASE = {
        'name': 'sdvor_stp',
        'engine': 'peewee.SqliteDatabase',
        'host': '10.0.16.101',
        'password': '1111',
        'user': 'bot',
        'engine': 'playhouse.postgres_ext.PostgresqlExtDatabase',
    }
    DEBUG = True
    SECRET_KEY = 'shhhh'
