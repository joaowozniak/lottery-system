from src.models.db import Lottery, Ticket
from src.utils.constants import Constants
from typing import Optional
import datetime
import random


class LotteryService:
    @staticmethod
    async def get_lottery(day: Optional[str]):
        if day == 'all':
            return await Lottery.objects.select_related("tickets").all()
        if not day:
            return await Lottery.objects.select_related("tickets").get(
                Lottery.created_at == datetime.datetime.today().strftime(Constants.DATE_FORMAT))
        return await Lottery.objects.get(Lottery.created_at == day)

    @staticmethod
    async def create_lottery(lottery: Lottery) -> Lottery:
        return await lottery.save()

    @staticmethod
    async def setup_lottery():
        previous_day = datetime.datetime.today() - datetime.timedelta(days=1)
        return await Lottery.objects.get_or_create(created_at=previous_day.strftime(Constants.DATE_FORMAT))

    @staticmethod
    async def new_lottery():
        return await Lottery.objects.get_or_create(created_at=datetime.datetime.now().strftime(Constants.DATE_FORMAT))

    @staticmethod
    async def get_current_lottery():
        return await Lottery.objects.get_or_none(
            created_at=datetime.datetime.today().strftime(Constants.DATE_FORMAT))

    @staticmethod
    async def get_closing_lottery() -> Lottery:
        previous_day = datetime.datetime.today() - datetime.timedelta(days=1)
        return await Lottery.objects.select_related("tickets").get_or_none(
            created_at=previous_day.strftime(Constants.DATE_FORMAT))

    @staticmethod
    async def assign_winner(closing_lottery: Lottery):
        tickets = await Ticket.objects.filter(created_at=closing_lottery.created_at).all()
        rand_winner_ticket_id = random.randint(0, len(tickets))
        winner = tickets[rand_winner_ticket_id]

        winner.is_winner = True
        await winner.upsert()

        closing_lottery.is_active = False
        closing_lottery.winning_ticket_id = winner.id
        await closing_lottery.upsert()

    async def manage_lottery_winner(self) -> None:
        # get closing lottery id
        closing_lottery = await self.get_closing_lottery()
        await closing_lottery.load()
        print(closing_lottery.id)
        print(closing_lottery is None)
        print(len(closing_lottery.tickets))
        if closing_lottery is not None and len(closing_lottery.tickets) > 0:
            print(f"Assigning lottery {closing_lottery.id} winner...")
            # close lottery and assign winner
            await self.assign_winner(closing_lottery)
        # create new lottery
        await self.new_lottery()
