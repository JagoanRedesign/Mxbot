"""
import requests
from pyrogram import *

from Mix import *

__modules__ = "Anime List"
__help__ = "Anime List"


@ky.ubot("anilist", sudo=True)
async def anilist_command(c: nlx, m):
    args = m.command
    if len(args) < 2:
        await m.reply("Please provide the ID of the anime.")
        return

    anime_id = args[1]

    url = f"https://api.jikan.moe/v4/anime/{anime_id}/videos"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data and "promo" in data:
            promos = data["promo"]
            for promo in promos:
                title = promo["title"]
                youtube_id = promo["trailer"]["youtube_id"]
                message_text = f"Title: {title}\nYouTube ID: {youtube_id}"
                await m.reply(message_text, reply_to_message_id=ReplyCheck(m))
        else:
            await m.reply("No promo videos found for this anime.")
    else:
        await m.reply(
            f"Failed to fetch data. Status code: {response.status_code}",
            reply_to_message_id=ReplyCheck(m),
        )
"""

import requests
from bs4 import BeautifulSoup
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Mix import *

__modles__ = "Anime Movie"
__help__ = "Anime Movie"


def get_streaming_link(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    player_option_title = soup.find("div", {"id": "player-option-7"}).span.text
    return player_option_title


@ky.ubot("anilist")
async def anilist_command(c: nlx, m):
    if len(m.command) < 2:
        await m.reply_text("Silakan masukkan judul anime setelah perintah /anilist.")
        return

    anime_title = " ".join(m.command[1:])
    url = f"https://samehadaku.email/{anime_title}/"
    response = requests.get(url)
    if response.status_code == 200:
        streaming_link = get_streaming_link(response.content)
        if streaming_link:
            reply_text = (
                f"Berikut adalah tautan untuk menonton {anime_title} di Samehadaku:"
            )
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Streaming di Samehadaku", url=streaming_link)]]
            )
            await m.reply_text(reply_text, reply_markup=reply_markup)
        else:
            await m.reply_text(
                f"Tidak dapat menemukan tautan streaming untuk {anime_title} di Samehadaku."
            )
    else:
        await m.reply_text(
            "Maaf, terjadi kesalahan saat mengambil informasi dari Samehadaku."
        )