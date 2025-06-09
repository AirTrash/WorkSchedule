from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


commands = {
    "/help": "посмотреть список доступных команд",
    "/users": "посмотреть пользователей",
    "/del_user <дежурный>": "удалить пользователя",
    "/add_user <дежурный>": "добавить пользователя",
    "/add_date <дата>": "добавить дату",
    "/del_date <дата>": "удалить дату",
    "/schedule [дата]": "посмотреть расписание",
    "/schedule_csv": "посмотреть расписание в файле формата csv",
    "/del_user_work <дата> <дежурный>": "удалить работу",
    "/set_user_work <дата> <дежурный> <работа>": "установить работу",
    "/add_chat <chat_id>": "добавить новый чат для отправки уведомлений",
    "/del_chat <chat_id>": "удалить чат для отправки уведомлений",
    "/chats": "отобразить чаты, в которые будет осуществляться отправка уведомлений",
    "/reload_schedule": "перезагрузить расписание из файла"
}


@router.message(F.text.in_({"/start", "/help"}))
async def start(message: Message):
    text = "Список доступных команд:\n"
    for command, desc in commands.items():
        text += command + " - " + desc + "\n"
    await message.reply(text)
