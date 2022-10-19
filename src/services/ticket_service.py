from src.models.db import Ticket


class TicketService:
    @staticmethod
    async def get_ticket(ticket_id: int) -> Ticket:
        return await Ticket.objects.get(Ticket.id == ticket_id)

    @staticmethod
    async def create_ticket(ticket: Ticket):
        return await ticket.save()
