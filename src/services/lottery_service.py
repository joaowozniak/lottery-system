from src.models.db import Lottery
from src.utils.constants import Constants
from typing import Optional
import datetime
import random


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
        previous_day = datetime.datetime.today() - datetime.timedelta(days=1)
        return await Lottery.objects.get_or_create(created_at=previous_day.today().strftime(Constants.DATE_FORMAT))

    @staticmethod
    async def get_current_lottery():
        return await Lottery.objects.get_or_none(created_at=datetime.datetime.today().strftime(Constants.DATE_FORMAT))

    @staticmethod
    async def get_closing_lottery() -> Lottery:
        previous_day = datetime.datetime.today() - datetime.timedelta(days=1)
        return await Lottery.objects.get_or_none(created_at=previous_day.strftime(Constants.DATE_FORMAT))

    @staticmethod
    async def assign_winner(closing_lottery: Lottery):
        rand_winner_ticket_id = random.randint(0, len(closing_lottery.tickets))
        closing_lottery.winning_ticket_id = rand_winner_ticket_id
        await closing_lottery.update()

    async def manage_lottery_winner(self) -> None:
        # get closing lottery id
        closing_lottery = await self.get_closing_lottery()
        await closing_lottery.load()
        if closing_lottery is not None and len(closing_lottery.tickets) > 0:
            print("Assigning lottery {} winner...", closing_lottery.id)
            # close lottery and assign winner
            await self.assign_winner(closing_lottery)
        # create new lottery
        await self.setup_lottery()
