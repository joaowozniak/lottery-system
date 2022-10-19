from fastapi import FastAPI
from typing import List
from src.models.db import database, User, Lottery, Ticket
from src.services.user_service import UserService
from src.services.lottery_service import LotteryService
from src.services.ticket_service import TicketService
from src.services.bet_service import BetService

app = FastAPI(title="Lottery-sys")
user_service = UserService
lottery_service = LotteryService
ticket_service = TicketService
bet_service = BetService


@app.get("/users", response_model=List[User])
async def read_users():
    return await user_service.get_users()


@app.post("/users", response_model=User)
async def create_user(user: User):
    return await user_service.create_user(user)


@app.get("/lottery", response_model=Lottery)
async def read_current_lottery(lottery_id: int):
    return await lottery_service.get_lottery(lottery_id)


@app.post("/lottery", response_model=Lottery)
async def create_lottery(lottery: Lottery):
    return await lottery_service.create_lottery(lottery)


@app.get("/ticket", response_model=Ticket)
async def read_ticket(ticket_id: int):
    return await ticket_service.get_ticket(ticket_id)


@app.post("/ticket", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    return await ticket_service.create_ticket(ticket)


@app.post("/bet")
async def bet():
    return await bet_service.place_bet("1", 1)


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
