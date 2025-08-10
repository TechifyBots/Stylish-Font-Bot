from asyncio import sleep
from .fonts import Fonts
from pyrogram import Client, filters
from pyrogram.types import *
from .maintenance import get_maintenance
from config import ADMIN

FONT_STYLES = [
    Fonts.typewriter,
    Fonts.outline,
    Fonts.serif,
    Fonts.bold_cool,
    Fonts.cool,
    Fonts.smallcap,
    Fonts.script,
    Fonts.bold_script,
    Fonts.tiny,
    Fonts.comic,
    Fonts.sans,
    Fonts.slant_san,
    Fonts.slant,
    Fonts.sim,
    Fonts.circles,
    Fonts.dark_circle,
    Fonts.gothic,
    Fonts.bold_gothic,
    Fonts.cloud,
    Fonts.happy,
    Fonts.sad,
    Fonts.special,
    Fonts.square,
    Fonts.dark_square,
    Fonts.andalucia,
    Fonts.manga,
    Fonts.stinky,
    Fonts.bubbles,
    Fonts.underline,
    Fonts.ladybug,
    Fonts.rays,
    Fonts.birds,
    Fonts.slash,
    Fonts.stop,
    Fonts.skyline,
    Fonts.arrows,
    Fonts.rvnes,
    Fonts.strike,
    Fonts.frozen,
]

@Client.on_message(filters.text & filters.private & ~filters.command(["start", "stats", "broadcast"]))
async def send_styled_fonts(client: Client, message: Message):
    if await get_maintenance() and message.from_user.id != ADMIN:
        return await message.reply_text("**🛠️ Bot is Under Maintenance**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support", user_id=int(ADMIN))]]))
    user_text = message.text
    for font_func in FONT_STYLES:
        try:
            styled_text = font_func(user_text)
            await client.send_message(
                chat_id=message.chat.id,
                text=styled_text,
                parse_mode=None
            )
            await sleep(0.2)
        except Exception as e:
            print(f"Error with {font_func.__name__}: {e}")
