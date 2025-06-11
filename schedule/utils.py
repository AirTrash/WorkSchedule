from datetime import datetime
from pandas import DataFrame, Series



def get_day(date: datetime):
    days = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье")
    return days[date.weekday()]


def format_once(day_schedule: Series):
    ret = ""
    for user in day_schedule.index:
        if day_schedule[user] is None: continue

        if "дежурный по оборудованию" in day_schedule[user].lower():
            emoji = ": 👷"
        else:
            emoji = ": 👨‍💻"
        ret += day_schedule[user] + emoji + user + "\n"
    return ret


def format_schedule(schedule: DataFrame) -> str:
    ret = ""
    for index in schedule.index:
        ret += "🗓" + get_day(index) + ", " + index.strftime("%d.%m.%Y") + "\n"
        ret += format_once(schedule.loc[index][1:]) + "\n"
    return ret
