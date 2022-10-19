import databases
import sqlalchemy
from typing import Optional
import ormar
import datetime as dt

from src.config.settings import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=128, unique=True, nullable=False)


class Ticket(ormar.Model):
    class Meta(BaseMeta):
        tablename = "tickets"

    id: int = ormar.Integer(primary_key=True)
    created_at: dt.datetime = ormar.DateTime(default=dt.datetime.utcnow)
    is_winner: bool = ormar.Boolean(default=False, nullable=False)
    user_id: Optional[User] = ormar.ForeignKey(User)
    lottery_id: int = ormar.Integer(default=None)


class Lottery(ormar.Model):
    class Meta(BaseMeta):
        tablename = "lotteries"

    id: int = ormar.Integer(primary_key=True)
    date_created: dt.datetime = ormar.DateTime(default=dt.datetime.utcnow)
    winning_ticket: Optional[Ticket] = ormar.ForeignKey(Ticket)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
