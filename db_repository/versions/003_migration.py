from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
channel = Table('channel', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=30)),
)

message = Table('message', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=200)),
    Column('created', DateTime),
    Column('user_id', Integer),
    Column('channel_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=20)),
    Column('pw_hash', String(length=100)),
    Column('channel_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['channel'].create()
    post_meta.tables['message'].columns['channel_id'].create()
    post_meta.tables['user'].columns['channel_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['channel'].drop()
    post_meta.tables['message'].columns['channel_id'].drop()
    post_meta.tables['user'].columns['channel_id'].drop()
