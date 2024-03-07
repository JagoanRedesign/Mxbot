from pyrogram.errors import *
from pyrogram.types import *

from Mix import *

__modles__ = "Join"
__help__ = """
Help Command Join 

• Perintah: <code>{0}join</code>
• Penjelasan: Untuk join ke Group atau Channel.
"""


@ky.ubot("join|masuk", sudo=True)
@ky.devs("Cjoin")
async def _(c, m):
    em = Emojik()
    em.initialize()
    Nan = m.command[1] if len(m.command) > 1 else m.chat.id
    ceger = await m.reply_text(f"{em.proses} <b>Processing...</b>")
    try:
        inpogc = await c.get_chat(Nan)
        namagece = inpogc.title

        await ceger.edit(
            f"{em.sukses} <b>Berhasil Bergabung ke</b> <code>{namagece}</code>"
        )
        await c.join_chat(Nan)
    except Exception as ex:
        await ceger.edit(f"{em.gagal} <b>ERROR: </b>\n\n<code>{str(ex)}</code>")


@ky.ubot("leave|kickme", sudo=True)
@ky.devs("Cleave")
async def _(c, m):
    em = Emojik()
    em.initialize()
    lus = m.command[1] if len(m.command) > 1 else m.chat.id
    inpogc = await c.get_chat(lus)
    namagece = inpogc.title
    ceger = await m.reply(f"{em.proses} <code>Processing...</code>")
    try:
        if str(lus) in NO_GCAST or inpogc.id in NO_GCAST:
            await ceger.edit(
                f"{em.gagal} <b>Tidak boleh menggunakan perintah itu di sini!</b>"
            )

        else:
            await c.leave_chat(lus)
            await ceger.edit(
                f"{em.sukses} {c.me.mention} Berhasil keluar dari <code>{namagece}</code><b>"
            )
    except pyrogram.errors.exceptions.bad_request_400.UserNotParticipant:
        await ceger.edit(
            f"{em.gagal} <b>Anda bukan anggota atau member di <code>{namagece}</code>"
        )
