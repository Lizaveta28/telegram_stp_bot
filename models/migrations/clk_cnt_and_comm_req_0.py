# Click count and comment required migration
from models.migrations.migrator import migrator
from playhouse.migrate import *

click_count = IntegerField(default=0)
comment_required = BooleanField(default=False)

migrate(
    migrator.add_column('type', 'click_count', click_count),
    migrator.add_column('type', 'comment_required', comment_required),
    migrator.add_column('section', 'click_count', click_count),
)