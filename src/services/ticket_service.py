from src.models.db import Ticket


class TicketService:
    @staticmethod
    async def get_ticket(ticket_id: int) -> Ticket:
        return await Ticket.objects.get(Ticket.id == ticket_id)

    @staticmethod
    async def create_ticket(ticket: Ticket):
        return await ticket.save()

    @staticmethod
    async def query_winning_ticket(day: str) -> Ticket:
        return await Ticket.objects.filter(Ticket.created_at == day, Ticket.is_winner == True).get()
