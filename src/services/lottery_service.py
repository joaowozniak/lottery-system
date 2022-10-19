from src.models.db import Lottery


class LotteryService:
    @staticmethod
    async def get_lottery(lottery_id: int) -> Lottery:
        return await Lottery.objects.get(Lottery.id == lottery_id)

    @staticmethod
    async def create_lottery(lottery: Lottery):
        return await lottery.save()
