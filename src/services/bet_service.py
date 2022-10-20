from src.services.ticket_service import TicketService
from src.models.db import Ticket, User, Lottery
from src.utils.constants import Constants
import datetime


class BetService:

    @staticmethod
    async def place_bet(username: str):
        user = await User.objects.get_or_create(username=username)
        await user.load()

        lottery = await Lottery.objects.get(created_at=datetime.datetime.today().strftime(Constants.DATE_FORMAT))
        await lottery.load()

        ticket = Ticket(user=user, lottery=lottery)
        return await TicketService.create_ticket(ticket)
