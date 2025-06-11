from typing import List

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

import conf
from schedule import schedule_manage
from schedule import utils as schedule_utils
from filters.command import ArgParse, date_parser

router = Router()


@router.message(Command("users"))
async def users(message: Message):
    users = ", ".join(schedule_manage.get_users())
    await message.reply("Список пользователей: " + users)


@router.message(Command("del_user"), ArgParse((str, )))
async def del_user(message: Message, args: List[str]):
    try:
        schedule_manage.del_user(args[0])
        await message.reply(f"Пользователь {args[0]} удален")
    except Exception as e:
        await message.reply("Не удалось удалить пользователя " + args[0])


@router.message(Command("add_user"), ArgParse((str, )))
async def add_user(message: Message, args: List[str]):
    try:
        schedule_manage.add_user(args[0])
        await message.reply(f"Пользователь {args[0]} добавлен")
    except Exception as e:
        await message.reply(f"Не удалось добавить пользователя {args[0]}")


@router.message(Command("schedule"), ArgParse((date_parser, ), 0))
async def schedule(message: Message, args: List):
    if len(args) == 0:
        sched = schedule_utils.format_schedule(schedule_manage.SCHEDULE)
        await message.reply("Текущее расписание:\n" + str(sched))
        return
    try:
        works = schedule_manage.get_date_works(args[0])
        text = schedule_utils.format_once(works)
        await message.reply(text)
    except Exception as e:
        await message.reply("Не удалось получить информацию за данную дату")


@router.message(Command("add_date"), ArgParse((date_parser, )))
async def add_date(message: Message, args: List):
    try:
        schedule_manage.add_date(args[0])
        await message.reply("Дата успешно добавлена")
    except Exception as e:
        print(e)
        await message.reply("Не удалось добавить дату")


@router.message(Command("del_date"), ArgParse((date_parser, )))
async def del_date(message: Message, args: List):
    try:
        schedule_manage.del_date(args[0])
        await message.reply("Дата успешно удалена")
    except Exception as e:
        await message.reply("Не удалось удалить дату")


@router.message(Command("del_user_work"), ArgParse((date_parser, str)))
async def del_user_work(message: Message, args: List):
    try:
        schedule_manage.del_user_work(args[0], args[1])
        await message.reply("Успешно удалено")
    except Exception as e:
        await message.reply("Не удалось, " + str(e))


@router.message(Command("set_user_work"))
async def set_user_work(message: Message):
    args = message.text.split(" ")
    if len(args) < 4:
        await message.reply("Неправильное количество аргументов")
        return

    try:
        date = date_parser(args[1])
        schedule_manage.set_user_work(date, args[2], " ".join(args[3:]))
        await message.reply("Успешно")
    except Exception as e:
        await message.reply("Не удалось, " + str(e))


@router.message(Command("schedule_csv"))
async def schedule_csv(message: Message):
    sched = FSInputFile(conf.SCHEDULE_PATH, filename="расписание.csv")
    await message.reply_document(sched, filename="расписание.csv")


@router.message(Command("reload_schedule"))
async def reload_schedule(message: Message):
    try:
        schedule_manage.reload()
        await message.reply("Данные загружены из файла")
    except Exception as e:
        print(e)
        await message.reply("Не удалось загрузить данные из файла, будут использоваться старые данные\nтекст ошибки: " + str(e))
