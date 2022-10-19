from src.services.lottery_service import LotteryService
from src.services.user_service import UserService
from src.services.ticket_service import TicketService
from src.models.db import Ticket


class BetService:
    @staticmethod
    async def place_bet(username: str, lottery_id: int):
        # check if username exists and get user id
        # check if lottery id exists
        # create and save new ticket
        user_id = 1
        lottery_id = 1

        ticket = Ticket(user_id=user_id, lottery_id=lottery_id)
        return await TicketService.create_ticket(ticket)
