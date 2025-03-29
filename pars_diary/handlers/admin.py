"""Админка.

Включает в себя информацию для админов:

- график прихода пользователей
- количество пользователей
- список рефералов
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from loguru import logger

from pars_diary.utils.db import GRAPH_NAME, GetStat, counter, get_graph
from pars_diary.utils.load_env import ADMINS_TG

router = Router(name="Admin commands")


@router.message(Command("admin"))
async def new_msg(msg: Message) -> None:
    """Отвечает за /admin."""
    logger.debug("[m] {}", msg.text)
    counter(msg.from_user.id, msg.text.split()[0][1:])

    # Если пользователь не админ - кусаемся
    if str(msg.from_user.id) not in ADMINS_TG:
        logger.warning("{} try to use /admin", msg.from_user.id)
        return

    # Обновляем график
    get_graph()

    # Получаем значения
    stat = GetStat()

    # Отвечаем пользователю
    await msg.answer_photo(
        FSInputFile(GRAPH_NAME),
        (
            f"<b>Всего пользователей: {stat.users_count}</b>\n\n"
            f"Авторизованных пользователей: {stat.cookie}\n\n"
            f"Уведомления: {stat.notify} / {stat.users_count}"
            f" ({stat.notify / stat.users_count * 100}%)\n"
            f"Умные уведомления: {stat.smart_notify} / {stat.users_count}"
            f" ({stat.smart_notify / stat.users_count * 100}%)\n\n"
            f"Использований комманды /about: {stat.command_about}\n"
            f"Использований комманды /admin: {stat.command_admin}\n"
            f"Использований комманды /birthdays: {stat.command_birthdays}\n"
            f"Использований комманды /ch: {stat.command_ch}\n"
            f"Использований комманды /cs: {stat.command_cs}\n"
            f"Использований комманды /events: {stat.command_events}\n"
            f"Использований комманды /hw: {stat.command_hw}\n"
            f"Использований комманды /i_marks: {stat.command_i_marks}\n"
            f"Использований комманды /marks: {stat.command_marks}\n"
            f"Использований комманды /me: {stat.command_me}\n"
            f"Использований комманды /new: {stat.command_new}\n"
            f"Использований комманды /notify: {stat.command_notify_settings}\n"
            f"Использований комманды /start: {stat.command_start}\n\n"
            "<b>Источники прихода аудитории (рефералы)"
            " (в порядке уменьшения выгоды):</b>\n\n"
            f"{stat.str_refer()}\n"
        ),
        parse_mode="HTML",
    )
