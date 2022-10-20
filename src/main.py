from fastapi import FastAPI
from src.services.lottery_service import LotteryService
from src.services.ticket_service import TicketService
from src.services.bet_service import BetService
from src.models.db import database, Ticket

app = FastAPI(title="Lottery-sys")
lottery_service = LotteryService
ticket_service = TicketService
bet_service = BetService


@app.post("/bet")
async def place_bet(username: str) -> Ticket:
    return await bet_service.place_bet(username)


@app.get("/winner")
async def get_day_winner_ticket(day: str):
    return await ticket_service.query_winning_ticket(day)


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
        await lottery_service.setup_lottery()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
