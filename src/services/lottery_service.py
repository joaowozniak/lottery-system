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
    async def close_lottery():
        print("current...")
        current = await Lottery.objects.get_or_none(is_active=True)
        current.is_active = False
        await current.update()

    @staticmethod
    async def setup_lottery():
        previous_day = datetime.datetime.today() - datetime.timedelta(days=1)
        today = datetime.datetime.today()
        return await Lottery.objects.get_or_create(created_at=today.strftime(Constants.DATE_FORMAT))

    @staticmethod
    async def new_lottery():
        today = datetime.datetime.now()
        tomorrow = today + datetime.timedelta(days=1)
        return await Lottery.objects.get_or_create(created_at=tomorrow.strftime(Constants.DATE_FORMAT), is_active=True)

    @staticmethod
    async def get_current_lottery():
        return await Lottery.objects.get_or_none(created_at=datetime.datetime.now().strftime(Constants.DATE_FORMAT),
                                                 is_active=True)

    @staticmethod
    async def get_closing_lottery() -> Lottery:
        # previous_day = datetime.datetime.today() - datetime.timedelta(days=1)

        # add control of just closed lottery
        return await Lottery.objects.select_related("tickets").get_or_none(
            created_at=datetime.datetime.now().strftime(Constants.DATE_FORMAT),
            is_active=True)

    async def manage_lottery_winner(self) -> None:
        print("Lottery closing...")
        closing_lottery = await self.get_closing_lottery()
        await closing_lottery.load()
        print(closing_lottery.id)
        print(closing_lottery is None)
        print(len(closing_lottery.tickets))
        if closing_lottery is not None:
            print(f"Verifying lottery {closing_lottery.id} winner...")
            # close lottery and assign winner
            await self.__assign_winner(closing_lottery)
        # create new lottery
        await self.new_lottery()
        print("New lottery created!")

    @staticmethod
    async def __assign_winner(closing_lottery: Lottery) -> None:
        print(f"Verifying tickets submitted for closing lottery {closing_lottery.id}...")
        tickets = await Ticket.objects.filter(created_at=closing_lottery.created_at).get_or_none()

        if tickets is not None:
            print(f"Found {len(tickets)} submitted.")
            rand_winner_ticket_id = random.randint(0, len(tickets))
            winner = tickets[rand_winner_ticket_id]
            winner.is_winner = True
            await winner.upsert()
            closing_lottery.winning_ticket_id = winner.id
            print(f"Ticket {winner.id} wins lottery {closing_lottery.id}.")

        else:
            print("Not tickets found.")

        closing_lottery.is_active = False
        await closing_lottery.upsert()
        print(f"Lottery {closing_lottery.id} of {closing_lottery.created_at} closed.")
