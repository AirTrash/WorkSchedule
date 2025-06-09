from pandas import Series

import conf
from .storage import BaseStorage, JSStorage
import schedule_manage
from datetime import datetime


class NotifierData:
    def __init__(self, storage: BaseStorage):
        self.storage = storage


    def add_chat_id(self, new_id):
        chat_ids = self.storage.get("chat_ids")
        chat_ids.append(new_id)
        self.storage.save("chat_ids", chat_ids)


    def get_chat_ids(self):
        return self.storage.get("chat_ids")


    def del_chat_id(self, chat_id):
        chat_ids = self.storage.get("chat_ids")
        chat_ids.remove(chat_id)
        self.storage.save("chat_ids", chat_ids)


notifier_data = NotifierData(JSStorage("notify/data.json"))


class Notifier:
    def __init__(self, bot, data: NotifierData):
        self.bot = bot
        self.data = data


    async def __notify_admin(self, msg: str):
        await self.bot.send_message(conf.ADMIN_ID, msg)


    async def notify_all_chats(self, works: Series):
        text = "На сегодняшний день:\n"
        for user in works.index:
            work = works[user] or "Отдых"
            text += user + " - " + work + "\n"
        for chat_id in self.data.get_chat_ids():
            try:
                await self.bot.send_message(chat_id, text)
            except Exception as e:
                await self.__notify_admin(f"Не удалось отправить оповещение в чат {chat_id}, текст ошибки: {e}")


    async def notify(self):
        try:
            now = datetime.now()
            today = datetime.strptime(f"{now.day}.{now.month}.{now.year}", "%d.%m.%Y")
            works = schedule_crud.get_date_works(today)
            await self.notify_all_chats(works)
        except Exception as e:
            await self.__notify_admin("Не удалось отправить уведомления для текущей даты, текст ошибки: " + str(e))
