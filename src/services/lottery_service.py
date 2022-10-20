from src.models.db import Lottery
from src.utils.constants import Constants
from typing import Optional
import datetime


class LotteryService:
    @staticmethod
    async def get_lottery(day: Optional[str]):
        if day == 'all':
            return await Lottery.objects.all()
        if not day:
            return await Lottery.objects.get(
                Lottery.created_at == datetime.datetime.today().strftime(Constants.DATE_FORMAT))
        return await Lottery.objects.get(Lottery.created_at == day)

    @staticmethod
    async def create_lottery(lottery: Lottery) -> Lottery:
        return await lottery.save()

    @staticmethod
    async def setup_lottery():
        return await Lottery.objects.get_or_create(created_at=datetime.datetime.today().strftime(Constants.DATE_FORMAT))
