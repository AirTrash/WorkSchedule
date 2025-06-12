import pandas as pd
from numpy import nan
from pandas import Series
from datetime import datetime, timedelta

import conf

from .utils import get_day


SCHEDULE: pd.DataFrame


def __save():
    SCHEDULE.to_csv(conf.SCHEDULE_PATH, date_format="%d.%m.%Y")


def load():
    global SCHEDULE
    SCHEDULE = pd.read_csv(conf.SCHEDULE_PATH)
    SCHEDULE["Дата"] = pd.to_datetime(SCHEDULE["Дата"], format="%d.%m.%Y")
    SCHEDULE.set_index("Дата", inplace=True)
    SCHEDULE.replace({nan: None}, inplace=True)

    for date in SCHEDULE.index:
        if SCHEDULE.loc[date, "ден нед"] is None:
            SCHEDULE.loc[date, "ден нед"] = get_day(date)
    else:
        __save()


def reload():
    global SCHEDULE
    schedule_back = SCHEDULE
    try:
        load()
    except Exception as e:
        SCHEDULE = schedule_back
        raise e


def get_users():
    return SCHEDULE.columns.values[1:]


def add_user(name: str):
    SCHEDULE.insert(len(SCHEDULE.columns.values), name, None)
    __save()


def del_user(name: str):
    SCHEDULE.drop(columns=name, inplace=True)
    __save()


def add_date(date: datetime):
    SCHEDULE.loc[date] = [get_day(date)] + [None for _ in range(len(SCHEDULE.columns.values) - 1)]
    SCHEDULE.sort_index(inplace=True)
    __save()


def del_date(date: datetime):
    SCHEDULE.drop(date, inplace=True)
    __save()


def set_user_work(date: datetime, user: str, new_work: str):
    if not SCHEDULE.index.isin([date]).any():
        raise KeyError("Даты " + str(date) + " нет в таблице")
    if not SCHEDULE.columns[1:].isin([user]).any():
        raise KeyError("Пользователя " + user + " не существует")

    SCHEDULE.loc[date, user] = new_work
    __save()


def del_user_work(date: datetime, user: str):
    if not SCHEDULE.index.isin([date]).any():
        raise KeyError("Даты " + str(date) + "нет в таблице")
    if not SCHEDULE.columns[1:].isin([user]).any():
        raise KeyError("Пользователя " + user + " не существует")
    SCHEDULE.loc[date, user] = None
    __save()


def get_date_works(date: datetime) -> Series:
    return SCHEDULE.loc[date][1:]


def get_weekly(date: datetime):
    dates = SCHEDULE.index.to_list()
    mon = date - timedelta(days=date.weekday())
    try:
        mon_idx = dates.index(mon)
    except Exception as e:
        raise ValueError(f"Для {date.strftime('%d.%m.%Y')} в таблице не найден ближайший понедельник")

    last_idx = mon_idx
    last_day = mon
    one_day = timedelta(days=1)
    for i in range(min(6, len(dates) - mon_idx)):
        next_day = last_day + one_day
        if next_day != dates[last_idx + 1]:
            break
        last_idx += 1
        last_day += one_day

    return SCHEDULE[mon_idx:last_idx+1]


load()
