#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import *
from helper_func import encode, admin

@Bot.on_message(filters.private & admin & ~filters.command(['start', 'commands','users','broadcast','batch', 'custom_batch', 'genlink','stats', 'dlt_time', 'check_dlt_time', 'dbroadcast', 'ban', 'unban', 'banlist', 'addchnl', 'delchnl', 'listchnl', 'fsub_mode', 'pbroadcast', 'add_admin', 'deladmin', 'admins']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)


@Bot.on_message(filters.private & ~admin & ~filters.command(['start', 'help']))
async def user_file_handler(client: Client, message: Message):
    try:
        await message.reply_photo(
            photo="https://i.postimg.cc/9FgztwCx/IMG-20250802-093723-437.jpg",  # আপনি চাইলে নিজের পিকচার দিতে পারেন
            caption=(
                "🚫 **ᴘᴇʀꜱᴏɴᴀʟ ʙᴏᴛ ɴᴏᴛɪᴄᴇ**\n\n"
                "ʏᴏᴜ ᴀʀᴇ ᴀᴛᴛᴇᴍᴘᴛɪɴɢ ᴛᴏ ᴜꜱᴇ ᴀ ʙᴏᴛ ᴛʜᴀᴛ ɪꜱ ʀᴇꜱᴇʀᴠᴇᴅ ꜰᴏʀ ᴘᴇʀꜱᴏɴᴀʟ ᴜꜱᴇ ᴏɴʟʏ.\n\n"
                "ʙᴜᴛ ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ! ᴡᴇ ʜᴀᴠᴇ ᴀ ᴘᴜʙʟɪᴄ ᴠᴇʀꜱɪᴏɴ ꜰᴏʀ ʏᴏᴜ ❤️\n\n"
                "📦 **ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴇᴀᴛᴜʀᴇꜱ ɪɴ ᴘᴜʙʟɪᴄ ʙᴏᴛ:**\n"
                "┏━━━━━━━━━━━━━━━┓\n"
                "┣ 🏅 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ\n"
                "┣ 🔗 ʟɪɴᴋ ꜱʜᴏʀᴛɴᴇʀ\n"
                "┣ ⏱️ ᴛᴏᴋᴇɴ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ\n"
                "┣ 🍿 ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ\n"
                "┣ 📢 ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ\n"
                "┣ 🎛️ ᴄᴜꜱᴛᴏᴍ ʙᴜᴛᴛᴏɴꜱ\n"
                "┣ ♻️ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ\n"
                "┣ 🔐 ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ\n"
                "┣ 📺 ꜱᴛʀᴇᴀᴍ/ᴅᴏᴡɴʟᴏᴀᴅ\n"
                "┗━━━━━━━━━━━━━━━┛\n\n"
                "✅ ʏᴏᴜ ᴄᴀɴ ᴄᴜꜱᴛᴏᴍɪᴢᴇ ᴇᴠᴇʀʏᴛʜɪɴɢ ꜰʀᴏᴍ ᴀ ᴛᴏ ᴢ, ꜱᴏ ᴅᴏɴ'ᴛ ᴅᴇʟᴀʏ, ᴛʀʏ ɪᴛ ɴᴏᴡ.👇"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 ᴏᴘᴇɴ ᴘᴜʙʟɪᴄ ʙᴏᴛ", url="https://t.me/File_Store_Prime_Bot")]
            ])
        )
    except Exception as e:
        print(e)
