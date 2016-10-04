from playhouse.migrate import *
from models.models import db


db
migrator = PostgresqlMigrator(db)