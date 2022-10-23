import asyncio
import time
from asyncio import ensure_future
from functools import wraps
from src.services.lottery_service import LotteryService


class SchedulerService:

    @staticmethod
    def lottery_scheduler(refresh_rate_in_seconds: float,
                          execution_hour: str):
        def decorator(func):

            @wraps(func)
            async def wrapped() -> None:
                async def loop() -> None:
                    while True:
                        current_time = time.strftime("%H:%M", time.localtime())
                        if current_time == execution_hour and \
                                await LotteryService.get_current_lottery() is not None:
                            print("No active lottery found")
                            try:
                                await func()
                            except Exception as exc:
                                raise exc
                        await asyncio.sleep(refresh_rate_in_seconds)

                ensure_future(loop())

            return wrapped

        return decorator
