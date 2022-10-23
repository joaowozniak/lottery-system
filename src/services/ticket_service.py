from fastapi import status
from fastapi.responses import JSONResponse
from src.models.db import Ticket, User


class TicketService:
    @staticmethod
    async def get_ticket(ticket_id: int) -> Ticket:
        return await Ticket.objects.get(Ticket.id == ticket_id)

    @staticmethod
    async def create_ticket(ticket: Ticket):
        return await ticket.save()

    @staticmethod
    async def query_winning_ticket(day: str) -> JSONResponse:
        winner = await Ticket.objects.filter(Ticket.created_at == day,
                                             Ticket.is_winner == True).get_or_none()

        if winner is not None:
            await winner.load()
            winner_user = await User.objects.filter(id=winner.user.id).get()
            winner.user = winner_user
            return winner

        return JSONResponse(
            content=f"FAILED: Winning ticket of {day} not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
