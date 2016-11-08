import config

class Configuration(object):
    DATABASE = {
        'name': config.db,
        'host': config.host,
        'password': config.password,
        'user': config.user,
        'engine': 'playhouse.postgres_ext.PostgresqlExtDatabase',
    }
    DEBUG = True
    SECRET_KEY = 'shhhh'
