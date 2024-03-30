import os

import aiofiles
import aiohttp
import requests
from pyquery import PyQuery as pq
from pyrogram import *

from Mix import *

__modles__ = "Pinterest"
__help__ = get_cgr("help_pint")


async def get_download_url_and_download(link, chat_id, caption=None):
    em = Emojik()
    em.initialize()
    try:
        post_request = requests.post(
            "https://www.expertsphp.com/download.php", data={"url": link}
        )
        request_content = post_request.content
        str_request_content = str(request_content, "utf-8")
        download_url = pq(str_request_content)("table.table-condensed")("tbody")("td")(
            "a"
        ).attr("href")

        if download_url is None:
            await nlx.send_message(chat_id, cgr("pint_3").format(em.gagal, link))
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as resp:
                if resp.status == 200:
                    file_path = f"pinterest_content"
                    async with aiofiles.open(file_path, mode="wb") as f:
                        await f.write(await resp.read())

                    if caption:
                        await nlx.send_photo(chat_id, file_path, caption=caption)
                    else:
                        await nlx.send_video(chat_id, file_path, caption=caption)

                    os.remove(file_path)

    except Exception as e:
        await nlx.send_message(chat_id, cgr("pint_4").format(em.gagal, str(e)))


@ky.ubot("pint", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    gue = c.me.mention
    try:
        url = m.text.split(maxsplit=1)[1]
        await get_download_url_and_download(
            url, m.chat.id, caption=cgr("pint_2").format(em.sukses, gue)
        )
        await pros.delete()
    except Exception as e:
        await m.reply(cgr("err").format(em.gagal, str(e)))
        await pros.delete()