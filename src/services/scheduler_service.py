import asyncio
import time
from functools import wraps
from src.services.lottery_service import LotteryService


class SchedulerService:
    @staticmethod
    def lottery_scheduler(refresh_rate_in_seconds: float, execution_hour: str):
        """
        Custom-made wrapper to schedule lottery restart between days
        :param refresh_rate_in_seconds: Rate at which it checks if it's execution time in seconds
        :param execution_hour: Restart execution hour with format "HH:MM"
        :return: Function wrapper
        """

        def decorator(func):
            @wraps(func)
            async def wrapped() -> None:
                async def loop() -> None:
                    while True:
                        current_time = time.strftime("%H:%M", time.localtime())
                        if (
                                current_time == execution_hour
                                and await LotteryService.get_current_lottery() is not None
                        ):
                            print("Found active lottery")
                            try:
                                await func()
                            except Exception as exc:
                                raise exc
                        await asyncio.sleep(refresh_rate_in_seconds)

                asyncio.create_task(loop())

            return wrapped

        return decorator
