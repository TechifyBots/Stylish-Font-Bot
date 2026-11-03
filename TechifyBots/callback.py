import html
import random
from pyrogram import Client, enums
from pyrogram.errors import MessageNotModified
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, WebAppInfo
from Script import text
from config import ADMIN, PICS, VERSION, PING_URL, SOURCE_CODE
from . import font
from .database import tb

@Client.on_callback_query()
async def callback_query_handler(client, query: CallbackQuery):
    data = query.data

    if data == "start":
        await query.message.edit_media(
            InputMediaPhoto(media=random.choice(PICS), caption=text.START.format(query.from_user.mention)),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('ℹ️ 𝖠𝖻𝗈𝗎𝗍', callback_data='about'), InlineKeyboardButton('📚 𝖧𝖾𝗅𝗉', callback_data='help')],
                [InlineKeyboardButton('🤖 𝖬𝗈𝗋𝖾 𝖡𝗈𝗍𝗌 🤖', url='https://telegram.me/TechifyBots/8', style=enums.ButtonStyle.PRIMARY)]
            ])
        )

    elif data == "help":
        await query.message.edit_media(
            InputMediaPhoto(media=random.choice(PICS), caption=text.HELP),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('👨‍💻 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋 👨‍💻', user_id=int(ADMIN))],
                [InlineKeyboardButton('↩️ 𝖡𝖺𝖼𝗄', callback_data="start", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton('❌ 𝖢𝗅𝗈𝗌𝖾', callback_data="close", style=enums.ButtonStyle.DANGER)]
            ])
        )

    elif data == "about":
        await query.message.edit_media(
            InputMediaPhoto(media=random.choice(PICS), caption=text.ABOUT.format(VERSION)),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('📂 𝖲𝗈𝗎𝗋𝖼𝖾 𝖢𝗈𝖽𝖾', url=SOURCE_CODE)],
                [InlineKeyboardButton('☕ 𝖣𝗈𝗇𝖺𝗍𝖾', callback_data='donate'),
                 InlineKeyboardButton('📊 𝖲𝗍𝖺𝗍𝗌', callback_data='stats')],
                [InlineKeyboardButton('↩️ 𝖡𝖺𝖼𝗄', callback_data='start', style=enums.ButtonStyle.PRIMARY)]
            ])
        )

    elif data == "donate":
        await query.message.edit_media(
            InputMediaPhoto(media=random.choice(PICS), caption=text.DONATE),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('💳 𝖲𝗎𝗉𝗉𝗈𝗋𝗍 𝖳𝗁𝖾 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋', web_app=WebAppInfo(url='https://techifybots.vercel.app/pay'))],
                [InlineKeyboardButton('↩️ 𝖡𝖺𝖼𝗄', callback_data='about', style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton('❌ 𝖢𝗅𝗈𝗌𝖾', callback_data='close', style=enums.ButtonStyle.DANGER)]
            ])
        )

    elif data == "stats":
        try:
            users = await tb.get_all_users()
            font_changes = await tb.get_font_changes()
            caption = text.STATS.format(font=font_changes, users=len(users))
        except Exception as e:
            caption = f"❌ **Unable to load statistics.**\n\n`{e}`"
        await query.message.edit_media(
            InputMediaPhoto(media=random.choice(PICS), caption=caption),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('🌐 𝖶𝖾𝖻𝗌𝗂𝗍𝖾', web_app=WebAppInfo(url=PING_URL))],
                [InlineKeyboardButton('↩️ 𝖡𝖺𝖼𝗄', callback_data='about', style=enums.ButtonStyle.PRIMARY),
                 InlineKeyboardButton('❌ 𝖢𝗅𝗈𝗌𝖾', callback_data='close', style=enums.ButtonStyle.DANGER)]
            ])
        )

    elif data == "close":
        await query.message.delete()

    elif data.startswith("fp:"):
        try:
            page = int(data.split(":", 1)[1])
        except ValueError:
            return await query.answer("Invalid page.", show_alert=True)
        if not 0 <= page < len(font.KB):
            return await query.answer("Invalid page.", show_alert=True)
        try:
            await query.message.edit_reply_markup(font.KB[page])
        except MessageNotModified:
            pass

    elif data.startswith("fs:"):
        key = data.split(":", 1)[1]
        if key not in font.STYLES:
            return await query.answer("Invalid font style.", show_alert=True)
        original = font.get_original_text(query.message)
        if original is None:
            return await query.answer("Original text not found! Send your text again.", show_alert=True)
        styled = font.convert(key, original)[:font.OUTPUT_MAX_LEN]
        try:
            await query.message.edit_text(
                f"<code>{html.escape(styled)}</code>\n\n👆 Click To Copy",
                reply_markup=query.message.reply_markup,
                parse_mode=font.ParseMode.HTML
            )
        except MessageNotModified:
            pass
        await tb.record_font_change()

    await query.answer()
