from typing import Optional
from src.models.db import Lottery, Ticket
from src.utils.constants import Constants
import datetime
import random


class LotteryService:
    @staticmethod
    async def get_lottery(day: Optional[str]):
        """
        Util function
        :param day:
        :return:
        """
        if day == "all":
            return await Lottery.objects.select_related("tickets").all()
        if not day:
            return await Lottery.objects.select_related("tickets").get(
                Lottery.created_at
                == datetime.datetime.today().strftime(Constants.DATE_FORMAT)
            )
        return await Lottery.objects.get(Lottery.created_at == day)

    @staticmethod
    async def create_lottery(lottery: Lottery) -> Lottery:
        """
        Saves lottery instance to database
        :param lottery: Lottery model instance to save
        :return: Lottery saved
        """
        return await lottery.save()

    @staticmethod
    async def close_lottery() -> None:
        """
        Closes day lottery
        :return:
        """
        current = await Lottery.objects.get_or_none(is_active=True)
        current.is_active = False
        await current.update()

    @staticmethod
    async def setup_lottery():
        """
        Setup lottery when app startup
        :return:
        """
        today = datetime.datetime.today()
        return await Lottery.objects.get_or_create(
            created_at=today.strftime(Constants.DATE_FORMAT)
        )

    @staticmethod
    async def new_lottery():
        """
        Creates next day lottery
        :return: Lottery
        """
        today = datetime.datetime.now()
        tomorrow = today + datetime.timedelta(days=1)
        return await Lottery.objects.get_or_create(
            created_at=tomorrow.strftime(Constants.DATE_FORMAT), is_active=True
        )

    @staticmethod
    async def get_current_lottery():
        """
        Returns current active lottery
        :return: Lottery
        """
        return await Lottery.objects.get_or_none(
            created_at=datetime.datetime.now().strftime(Constants.DATE_FORMAT),
            is_active=True,
        )

    @staticmethod
    async def get_closing_lottery() -> Lottery:
        """
        Returns lottery to close
        :return: Lottery
        """
        return await Lottery.objects.select_related("tickets").get_or_none(
            created_at=datetime.datetime.now().strftime(Constants.DATE_FORMAT),
            is_active=True,
        )

    async def manage_lottery_winner(self) -> None:
        """
        Orchestrates process of closing day lottery, assing winner, open following day lottery
        :return:
        """
        print("Lottery closing...")
        closing_lottery = await self.get_closing_lottery()
        await closing_lottery.load()

        if closing_lottery is not None:
            print(f"Verifying lottery {closing_lottery.id} winner...")
            # close lottery and assign winner
            await self.__assign_winner(closing_lottery)
        # create new lottery
        await self.new_lottery()
        print("New lottery created!")

    @staticmethod
    async def __assign_winner(closing_lottery: Lottery) -> None:
        """
        Assings lottery winner randomly
        :param closing_lottery: Lottery instance to close
        :return:
        """
        print(
            f"Verifying tickets submitted for closing lottery {closing_lottery.id}..."
        )
        tickets = await Ticket.objects.filter(
            created_at=closing_lottery.created_at
        ).get_or_none()

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
