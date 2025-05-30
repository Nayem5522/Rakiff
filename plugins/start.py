# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *

BAN_SUPPORT = f"{BAN_SUPPORT}"

#async def is_subscribedp(bot, query, channel):
#    btn = []
#    for id in channel:
#        chat = await bot.get_chat(int(id))
#        try:
#            await bot.get_chat_member(id, query.from_user.id)
#        except UserNotParticipant:
#            btn.append([InlineKeyboardButton(f"✇ Join {chat.title} ✇", url=chat.invite_link)]) #✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇
#        except Exception as e:
#            pass
#    return btn

async def is_subscribedp(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            # চেক করা হচ্ছে চ্যানেল প্রাইভেট না পাবলিক
            if chat.username:  # পাবলিক চ্যানেল
                join_url = f"https://t.me/{chat.username}"
                btn.append([InlineKeyboardButton(f"✇ Join {chat.title} ✇", url=join_url)])
            else:  # প্রাইভেট চ্যানেল
                try:
                    invite_link = chat.invite_link
                    if not invite_link:
                        invite_link = await bot.export_chat_invite_link(id)
                    btn.append([InlineKeyboardButton(f"✇ Request to Join {chat.title} ✇", url=invite_link)])
                except Exception as e:
                    print(f"Couldn't get invite link: {e}")
        except Exception as e:
            print(f"Error checking member: {e}")
    return btn
    

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if user is banned
    banned_users = await db.get_ban_users()
    if user_id in banned_users:
        return await message.reply_text(
            "<b>⛔️ You are Bᴀɴɴᴇᴅ from using this bot.</b>\n\n"
            "<i>Contact support if you think this is a mistake.</i>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Contact Support", url=BAN_SUPPORT)]]
            )
        )
    # ✅ Check Force Subscription
            
    if not await is_subscribed(client, user_id):
        #await temp.delete()
        return await not_joined(client, message)

    # File auto-delete time in seconds (Set your desired time in seconds here)
    FILE_AUTO_DELETE = await db.get_del_timer()  # Example: 3600 seconds (1 hour)

    # Add user if not already present
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except:
            pass

    # Handle normal message flow
    text = message.text
    if len(text) > 7:
        if AUTH_CHANNEL:
            try:
                btn = await is_subscribedp(client, message, AUTH_CHANNEL)
                if btn:
                    username = (await client.get_me()).username
                    if len(message.command) > 1:
                        btn.append([InlineKeyboardButton("♻️ ʀᴇғʀᴇsʜ ♻️", url=f"https://t.me/{username}?start={message.command[1]}")])
                    else:
                        btn.append([InlineKeyboardButton("♻️ ʀᴇғʀᴇsʜ ♻️", url=f"https://t.me/{username}?start=true")])

                    await message.reply_photo(
                        photo="https://i.postimg.cc/7Zpf9s1C/IMG-20250514-223544-954.jpg",  # Replace with your image link
                        caption = (
                            f"<b>👋 Hello {message.from_user.mention},\n\n"
                            "<b>🗃️ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ꜰɪʟᴇ ʏᴏᴜ ʀᴇǫᴜᴇsᴛᴇᴅ, ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟs! 📢</b>\n\n"
                            "1️⃣ ғɪʀsᴛ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ <b>\"ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟs\"</b> ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ.  \n"
                            "2️⃣ ᴛʜᴇɴ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ <b>\"ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ\"</b> ᴏʀ <b>\"ᴊᴏɪɴ\"</b> ɪɴ ᴇᴀᴄʜ ᴄʜᴀɴɴᴇʟ.  \n"
                            "3️⃣ ᴀғᴛᴇʀ ᴊᴏɪɴɪɴɢ ᴀʟʟ ᴄʜᴀɴɴᴇʟs, ᴄʟɪᴄᴋ ᴛʜᴇ <b>\"ʀᴇғʀᴇsʜ\" 🔄</b> ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ᴀᴄᴄᴇss.\n\n"
                            "⚠️ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ᴍᴜsᴛ ʙᴇ ᴊᴏɪɴᴇᴅ ғᴏʀ ᴀᴄᴄᴇss.\n\n"
                            "---\n\n"
                            "<b>🗃️ ফাইল পেতে হলে অবশ্যই আমাদের অফিসিয়াল সব চ্যানেলে যুক্ত হতে হবে! 📢</b>\n\n"
                            "1️⃣ প্রথমে নিচের <b>\"Join Update Channels\"</b> বাটনে ক্লিক করুন।  \n"
                            "2️⃣ তারপর প্রতিটি চ্যানেলে গিয়ে <b>\"Request to Join\"</b> বা <b>\"Join\"</b> বাটনে ক্লিক করুন।  \n"
                            "3️⃣ সব চ্যানেলে যুক্ত হওয়ার পর নিচের <b>\"Refresh\" 🔄</b> বাটনে ক্লিক করুন পরবর্তী এক্সেস পেতে।\n\n"
                            "⚠️ যতগুলো চ্যানেল দেখাবে, সবগুলোতে অবশ্যই যোগ দিতে হবে।\n\n"
                            "ধন্যবাদ আপনার সহযোগিতার জন্য! 😊\n"
                            "ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ʏᴏᴜʀ ᴄᴏᴏᴘᴇʀᴀᴛɪᴏɴ! ♥️"
                        ),
                        reply_markup=InlineKeyboardMarkup(btn)
                    )
                    return
            except Exception as e:
                print(e)
        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            return

        string = await decode(base64_string)
        argument = string.split("-")

        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except Exception as e:
                print(f"Error decoding IDs: {e}")
                return

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error decoding ID: {e}")
                return

        temp_msg = await message.reply("<b>Please wait...</b>")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text("Something went wrong!")
            print(f"Error getting messages: {e}")
            return
        finally:
            await temp_msg.delete()
 
        codeflix_msgs = []

        for msg in messages:
            # Try to get internal file name from different media types
            file_name = None
            file_size = None
            
            if msg.document:
                file_name = msg.document.file_name
                file_size = msg.document.file_size
            elif msg.video:
                file_name = msg.video.file_name
                file_size = msg.video.file_size
            elif msg.audio:
                file_name = msg.audio.file_name
                file_size = msg.audio.file_size
            elif msg.animation:
                file_name = msg.animation.file_name
                file_size = msg.animation.file_size
            elif msg.voice:
                file_name = "Voice Message"
                file_size = msg.voice.file_size
            elif msg.video_note:
                file_name = "Video Note"
                file_size = msg.video_note.file_size

            formatted_size = (
    f"╭─────────────⍟\n"
    f"├📦 ꜰɪʟᴇ sɪᴢᴇ : {format_size(file_size)}\n"
    f"╰─────────────⍟\n"
) if file_size else ""
            # Use file_name if exists, else use original caption
            original_caption = file_name if file_name else (msg.caption.html if msg.caption else "")
            caption = f"<b>🗃️ ꜰɪʟᴇ ɴᴀᴍᴇ : </b> @PrimeCineHub <a href='https://t.me/PrimeCineZone'>{original_caption}</a>\n\n{formatted_size}{CUSTOM_CAPTION}" if CUSTOM_CAPTION else original_caption

            # Custom Buttons
            custom_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🍿 ᴘʀɪᴍᴇ ᴄɪɴᴇᴢᴏɴᴇ", url="https://t.me/PrimeCineZone"),
        InlineKeyboardButton("〄 ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ", url="https://t.me/Prime_Botz")
    ],
    [InlineKeyboardButton("🔍 ᴘʀɪᴍᴇ ʀᴇQᴜᴇꜱᴛ ɢʀᴏᴜᴘ 🎬", url="https://t.me/PrimeCineZone/143")]
])

            try:
                snt_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=custom_buttons,
                    protect_content=PROTECT_CONTENT
                )
                await asyncio.sleep(0.5)
                codeflix_msgs.append(snt_msg)

            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=custom_buttons,
                    protect_content=PROTECT_CONTENT
                )
                codeflix_msgs.append(copied_msg)

            except:
                pass

        if FILE_AUTO_DELETE > 0:
            notification_msg = await message.reply(
                f"""<b>⚠️ 𝐍𝐨𝐭𝐢𝐜𝐞 | বিজ্ঞপ্তি ⚠️

🕒 Tʜɪs ғɪʟᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ɪɴ {get_exp_time(FILE_AUTO_DELETE)}.  
🕒 এই ফাইলটি {get_exp_time(FILE_AUTO_DELETE)} এর মধ্যে স্বয়ংক্রিয়ভাবে মুছে যাবে।

📤 Pʟᴇᴀsᴇ sᴀᴠᴇ ᴏʀ sʜᴀʀᴇ ᴏʀ ғᴏʀᴡᴀʀᴅ ɪᴛ sᴏᴍᴇᴡʜᴇʀᴇ ᴇʟsᴇ ʙᴇғᴏʀᴇ ɪᴛ ɢᴇᴛs ᴅᴇʟᴇᴛᴇᴅ.  
📤 মুছে যাওয়ার আগে অনুগ্রহ করে এটি অন্য কোথাও শেয়ার বা ফরোয়ার্ড করে রাখুন।

✅ Tʜᴀɴᴋ Yᴏᴜ ғᴏʀ / ধন্যবাদ  
– <i>@PrimeCineZone & @Prime_Botz</i></b>"""
            )

            await asyncio.sleep(FILE_AUTO_DELETE)

            for snt_msg in codeflix_msgs:    
                if snt_msg:
                    try:    
                        await snt_msg.delete()  
                    except Exception as e:
                        print(f"Error deleting message {snt_msg.id}: {e}")

            try:
                reload_url = (
                    f"https://t.me/{client.username}?start={message.command[1]}"
                    if message.command and len(message.command) > 1
                    else None
                )
                keyboard = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=reload_url)]]
                ) if reload_url else None

                await notification_msg.edit(
                    "<b>ʏᴏᴜʀ ᴠɪᴅᴇᴏ / ꜰɪʟᴇ ɪꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ !!\n\nᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴅᴇʟᴇᴛᴇᴅ ᴠɪᴅᴇᴏ / ꜰɪʟᴇ 👇</b>",
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating notification with 'Get File Again' button: {e}")
    else:
        reply_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🔎 ʀᴇǫᴜᴇsᴛ ɢʀᴏᴜᴘ 🎞️", url="https://t.me/+OG3sftDEbZ9kMzFl"),
        InlineKeyboardButton("〄 ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ 〄", url="https://t.me/Prime_Botz")
    ],
    [
        InlineKeyboardButton("🍿 ᴘʀɪᴍᴇ ᴄɪɴᴇᴢᴏɴᴇ 🗃️", url="https://t.me/PrimeCineHub")
    ],
    [
        InlineKeyboardButton("〆 ʜᴇʟᴘ 〆", callback_data='help'),
        InlineKeyboardButton("〆 ᴀʙᴏᴜᴛ 〆", callback_data='about')
    ],
    [
        InlineKeyboardButton("✧ ᴄʀᴇᴀᴛᴏʀ ✧", url="https://t.me/Prime_Nayem")
    ]
])
        await message.reply_photo(
            photo=START_PIC,
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            message_effect_id=5104841245755180586)  # 🔥
        
        return



#=====================================================================================##
# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport



# Create a global dictionary to store chat data
chat_data_cache = {}

async def not_joined(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>")

    user_id = message.from_user.id
    buttons = []
    count = 0

    try:
        all_channels = await db.show_channels()  # Should return list of (chat_id, mode) tuples
        for total, chat_id in enumerate(all_channels, start=1):
            mode = await db.get_channel_mode(chat_id)  # fetch mode 

            await message.reply_chat_action(ChatAction.TYPING)

            if not await is_sub(client, user_id, chat_id):
                try:
                    # Cache chat info
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]
                    else:
                        data = await client.get_chat(chat_id)
                        chat_data_cache[chat_id] = data

                    name = data.title

                    # Generate proper invite link based on the mode
                    if mode == "on" and not data.username:
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                            )
                        link = invite.invite_link

                    else:
                        if data.username:
                            link = f"https://t.me/{data.username}"
                        else:
                            invite = await client.create_chat_invite_link(
                                chat_id=chat_id,
                                expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None)
                            link = invite.invite_link

                    buttons.append([InlineKeyboardButton(text=name, url=link)])
                    count += 1
                    await temp.edit(f"<b>{'! ' * count}</b>")

                except Exception as e:
                    print(f"Error with chat {chat_id}: {e}")
                    return await temp.edit(
                        f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @Prime_Admin_Support_ProBot</i></b>\n"
                        f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
                    )

        # Retry Button
        try:
            buttons.append([
                InlineKeyboardButton(
                    text='♻️ Tʀʏ Aɢᴀɪɴ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ])
        except IndexError:
            pass

        await message.reply_photo(
            photo=FORCE_PIC,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except Exception as e:
        print(f"Final Error: {e}")
        await temp.edit(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @Prime_Admin_Support_ProBot</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
        )

#=====================================================================================##

@Bot.on_message(filters.command('commands') & filters.private & admin)
async def bcmd(bot: Bot, message: Message):        
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])
    await message.reply(text=CMD_TXT, reply_markup = reply_markup, quote= True)
