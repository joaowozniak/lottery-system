from typing import Optional, List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.config.settings import settings
from src.models.db import database, Ticket, User, Lottery
from src.services.bet_service import BetService
from src.services.lottery_service import LotteryService
from src.services.ticket_service import TicketService
from src.services.user_service import UserService
from src.services.scheduler_service import SchedulerService

app = FastAPI(
    title="Lottery-system",
    description="Lottery system that allows users to submit lottery ballots for any lottery",
)

lottery_service = LotteryService()
ticket_service = TicketService()
bet_service = BetService()
user_service = UserService()


@app.post(
    "/users",
    summary="Create new users",
    description="Allow user to participate in lottery",
    name="POST new user to lottery-system",
)
async def create_user(user: User) -> JSONResponse:
    return await user_service.create_user(user)


@app.post(
    "/bet",
    summary="Submit new lottery ballot",
    description="Allow user to submit lottery ballot",
    name="POST new bet to Storage-Api",
)
async def place_bet(username: str) -> JSONResponse:
    return await bet_service.place_bet(username)


@app.get(
    "/winner",
    summary="Get winner ticket",
    description="Allow user to query wining ballot for date",
    name="GET winning ticker of Storage-Api",
)
async def get_day_winner_ticket(day: str) -> JSONResponse:
    return await ticket_service.query_winning_ticket(day)


@app.on_event("startup")
async def startup():
    print("Starting application...")
    if not database.is_connected:
        await database.connect()
        await lottery_service.setup_lottery()
    await schedule_lottery_restart()


@SchedulerService.lottery_scheduler(
    refresh_rate_in_seconds=settings.refresh_rate, execution_hour=settings.exec_hour
)
async def schedule_lottery_restart():
    await lottery_service.manage_lottery_winner()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


##############################################
# Utils Endpoints
##############################################
@app.get("/users", response_model=List[User])
async def read_users():
    return await user_service.get_users()


@app.get("/lottery")
async def get_lottery(day: Optional[str]):
    return await lottery_service.get_lottery(day)


@app.post("/lottery", response_model=Lottery)
async def create_lottery(lottery: Lottery):
    return await lottery_service.create_lottery(lottery)


@app.get("/ticket", response_model=Ticket)
async def read_ticket(ticket_id: int):
    return await ticket_service.get_ticket(ticket_id)


@app.post("/ticket", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    return await ticket_service.create_ticket(ticket)
