import asyncio
from aiogram import Dispatcher, Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import notify.notifier
from handlers.schedule_commands import router as schedule_router
from handlers.base_commands import router as base_router
from handlers.notifier_commands import router as notify_router
import conf

from notify.notifier import Notifier, notifier_data


class AdminFilter(BaseFilter):
    def __init__(self, admin_id: int):
        self.admin_id = admin_id


    async def __call__(self, message: Message):
        return message.from_user.id == self.admin_id


def init_admin_filters(*routers):
    for router in routers:
        router.message.filter(AdminFilter(conf.ADMIN_ID))


def schedule_notifies(bot: Bot):
    notifier = Notifier(bot, notifier_data)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        notifier.notify,
        "cron",
        hour=9,
        minute=0
    )
    scheduler.add_job(
        notifier.weekly_notify,
        "cron",
        hour=9,
        minute=0,
        day_of_week=0
    )
    scheduler.start()
    return scheduler


async def main():
    bot = Bot(token=conf.TOKEN)

    schedule_notifies(bot)

    dp = Dispatcher()
    init_admin_filters(base_router, notify_router, schedule_router)
    dp.include_routers(base_router, notify_router, schedule_router)

    print("start bot")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
