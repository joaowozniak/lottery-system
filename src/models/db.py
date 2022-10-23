from src.utils.constants import Constants
from src.config.settings import settings
from typing import Optional
import datetime
import databases
import sqlalchemy
import ormar

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


class Lottery(ormar.Model):
    class Meta(BaseMeta):
        tablename = "lotteries"

    id: int = ormar.Integer(primary_key=True)
    created_at: str = ormar.String(max_length=128, default=datetime.datetime.today().strftime(Constants.DATE_FORMAT))
    winning_ticket_id: int = ormar.Integer(default=0)
    is_active: bool = ormar.Boolean(default=True)


class Ticket(ormar.Model):
    class Meta(BaseMeta):
        tablename = "tickets"

    id: int = ormar.Integer(primary_key=True)
    created_at: str = ormar.String(max_length=128, default=datetime.datetime.today().strftime(Constants.DATE_FORMAT))
    is_winner: bool = ormar.Boolean(default=False, nullable=False)
    user: Optional[User] = ormar.ForeignKey(User)
    lottery: Optional[Lottery] = ormar.ForeignKey(Lottery)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
