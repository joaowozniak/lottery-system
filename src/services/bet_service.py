from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from src.services.ticket_service import TicketService
from src.models.db import Ticket, User, Lottery


class BetService:

    async def place_bet(self, username: str) -> JSONResponse:
        """
        Submits lottery ballot to ongoing lottery
        :param username: Unique username
        :return: Ticket created
        """
        print("Submitting new bet...")

        user = await self.__verify_user(username)
        lottery = await self.__verify_lottery()
        ticket = Ticket(user=user, lottery=lottery)

        return await TicketService.create_ticket(ticket)

    @staticmethod
    async def __verify_user(username: str) -> User:
        """
        User verification in database
        :param username:
        :return: User model
        """
        user = await User.objects.get_or_none(username=username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"FAILED: Username {username} not found. Register first.",
            )

        await user.load()
        return user

    @staticmethod
    async def __verify_lottery() -> Lottery:
        """
        Lottery verification in database
        :return: Lottery model
        """
        lottery = await Lottery.objects.get_or_none(is_active=True)

        if lottery is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lottery not active.",
            )

        await lottery.load()
        return lottery
