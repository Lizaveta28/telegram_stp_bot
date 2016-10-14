# Click count and comment required migration
from models.migrations.migrator import migrator
from playhouse.migrate import *

add_text = TextField(null=True)

migrate(
    migrator.add_column('stprequest', 'add_text', add_text),
)