from typing import List, Tuple, Callable, Dict, Any

from datetime import datetime

from aiogram.filters import BaseFilter
from magic_filter.magic import MagicFilter
from aiogram.types import Message


class ArgParse(BaseFilter):
    def __init__(self, args: List[Callable] | Tuple[Callable, ...], min_count: int | None = None):
        self.args = args
        if min_count is None:
            self.min_count = len(args)
        else:
            self.min_count = min_count


    async def __call__(self, message: Message ) -> bool | Dict[str, Any]:
        args = message.text.split(" ")
        if len(args) - 1 < self.min_count or len(args) - 1 > len(self.args):
            await message.reply(f"Неверное количество аргументов, передано: {len(args) - 1}, ожидалось: от {self.min_count} до {len(self.args)}")
            return False

        ret = []
        for i in range(0, max(len(args) - 1, self.min_count)):
            try:
                checker = self.args[i]
                arg = args[i + 1]
                result = checker(arg)
                ret.append(result)
            except ValueError as e:
                await message.reply(f"Аргумент {i + 1} не корректен, {e}")
                return False
        return {"args": ret}


def date_parser(arg: str, format: str = "%d.%m.%Y"):
    try:
        date = datetime.strptime(arg, format)
    except Exception as e:
        raise ValueError(f"Дата {arg} не соответствует формату {format}")
    return date
