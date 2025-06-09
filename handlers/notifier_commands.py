from typing import List

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from notify.notifier import notifier_data
from filters.command import ArgParse


router = Router()


@router.message(Command("chats"))
async def chats(message: Message):
    await message.reply(
        "Список чатов, в которые осуществляется отправка уведомлений: " +
        " ".join((str(id) for id in notifier_data.get_chat_ids()))
    )


@router.message(Command("add_chat"), ArgParse((int, )))
async def add_chat(message: Message, args: List):
    try:
        notifier_data.add_chat_id(args[0])
        await message.reply(f"Чат {args[0]} добавлен")
    except Exception as e:
        print(e)
        await message.reply("Не удалось добавить новый чат")


@router.message(Command("del_chat"), ArgParse((int, )))
async def del_chat(message: Message, args: List):
    try:
        notifier_data.del_chat_id(args[0])
        await message.reply(f"Чат {args[0]} удален")
    except Exception as e:
        await message.reply(f"Не удалось удалить чат {args[0]}, возможно он уже удален")
