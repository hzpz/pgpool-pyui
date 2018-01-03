"""pgpool-pyui model"""
import logging

from peewee import Model, Proxy, \
    CharField, DateTimeField, SmallIntegerField, BooleanField, ForeignKeyField
from playhouse.db_url import connect

LOG = logging.getLogger(__name__)

DATABASE = Proxy()


class BaseModel(Model):
    """Base model for all entities"""

    class Meta:
        """Meta class needed for peewee"""
        database = DATABASE


class Account(BaseModel):
    """Database model for account"""
    auth_service = CharField()
    username = CharField(primary_key=True)
    password = CharField()
    last_modified = DateTimeField()
    system_id = CharField()
    level = SmallIntegerField()
    banned = BooleanField()
    shadowbanned = BooleanField()
    lures = SmallIntegerField()

    def get_status(self):
        """Returns the status of the account, i.e. 'good', 'only blind' or 'banned'"""
        if not self.banned and not self.shadowbanned:
            return 'good'
        elif not self.banned and self.shadowbanned:
            return 'only blind'
        elif self.banned:
            return 'banned'
        else:
            return 'unknown'

    def __repr__(self):
        return "%s (Lv. %s): %s" % (self.username, self.level, self.get_status())


class Event(BaseModel):
    """Database model for event"""
    timestamp = DateTimeField()
    description = CharField()
    entity = ForeignKeyField(Account, related_name='events')

    def __repr__(self):
        return "(%s) %s: %s" % (self.timestamp, self.entity.username, self.description)  # pylint: disable=no-member


def init_db(database_url):
    """Initializes the database with the given URL, will NOT actually connect to the database"""
    LOG.info("Initializing database from URL: %s", database_url)
    database = connect(database_url)
    DATABASE.initialize(database)


def create_tables():
    """FOR TESTING ONLY: Creates tables in the database"""
    LOG.info("Creating tables")
    try:
        DATABASE.connect()
        DATABASE.create_tables([Account, Event], safe=True)
    finally:
        DATABASE.close()
