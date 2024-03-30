import re

import requests
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Mix import *

__modles__ = "Anime Streaming"
__help__ = "Anime Streaming"


URL_REGEX = re.compile(
    r"""(?i)\b((?:https?://|www\d{0,3}[.]|
                          [a-z0-9.\-][.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|
                          (\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\
                          ()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""".strip()
)


def get_streaming_links(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/streaming"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data", [])
        return data
    else:
        return []


@ky.ubot("streaming", sudo=True)
async def send_streaming_links(c: nlx, m):
    if len(m.command) > 1:
        anime_name = m.command[1]
        anime_id = anime_to_id(anime_name.lower())
        if anime_id:
            streaming_links = get_streaming_links(anime_id)
            if streaming_links:
                buttons_list = [
                    (link_data["name"], link_data["url"])
                    for link_data in streaming_links
                ]
                keyboard_markup = create_keyboard(buttons_list)
                await m.reply_text(
                    "Pilih platform streaming:", reply_markup=keyboard_markup
                )
            else:
                await m.reply_text(
                    "Tidak ada informasi streaming untuk anime tersebut.",
                    reply_markup=InlineKeyboardMarkup([]),
                )
        else:
            await m.reply_text("Anime tidak ditemukan.")
    else:
        await m.reply_text("Format perintah salah. Gunakan /streaming [Nama Anime]")


def create_keyboard(buttons_list):
    keyboard_data = dict()
    for text, data in buttons_list:
        keyboard_data[text] = data

    return ikb(keyboard_data)


def ikb(data, row_width=2):
    buttons = []
    for text, data in data.items():
        if is_url(data):
            buttons.append(InlineKeyboardButton(text, url=data))
        else:
            buttons.append(InlineKeyboardButton(text, callback_data=data))
    keyboard_markup = InlineKeyboardMarkup([buttons])
    print("Keyboard Markup:", keyboard_markup)
    return keyboard_markup


def is_url(text):
    return bool(URL_REGEX.search(text))


def anime_to_id(anime_name):
    anime_dict = {
        "naruto": 20,
        "attack on titan": 16498,
        "one piece": 21,
        "demon slayer": 38000,
        "my hero academia": 38408,
        "death note": 1535,
        "fullmetal alchemist": 5114,
        "sword art online": 11757,
        "one punch man": 30276,
        "tokyo ghoul": 22319,
    }
    return anime_dict.get(anime_name, None)
