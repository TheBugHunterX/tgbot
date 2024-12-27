import os
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.modules.re_link import RE_LINK
from bot.modules.archive.ytdl import PYTUBE


async def func_add_download_ytdl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = update.message.reply_to_message
    url = re_msg.text if re_msg else " ".join(context.args)

    if chat.type != "private":
        _bot_info = await LOCAL_DATABASE.find("_bot_info")
        btn_data = {
            "Start me in private": f"{_bot_info.get('link')}?start=start"
        }
        btn = await Button.ubutton(btn_data)
        await Message.reply_msg(update, f"This function has some limitaions.\nYou can use it in pm.", btn=btn)
        return
    
    if not url:
        await Message.reply_msg(update, "Use <code>/ytdl youtube_url</code> to download a video!")
        return
    
    youtube_domains = ["youtube.com", "youtu.be"]
    domain = await RE_LINK.get_domain(url)
    if domain not in youtube_domains:
        await Message.reply_msg(update, "Please send a valid youtube video link!")
        return
    
    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "users",
        "db_find": "user_id",
        "db_vlaue": user.id,
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": e_msg.id,
        "edit_data_value_msg_pointer_id": None
    }

    await LOCAL_DATABASE.insert_data("data_center", user.id, data)
    
    btn_data_row1 = {
        "Video (mp4)": "mp4",
        "Audio (mp3)": "mp3"
    }

    btn_data_row2 = {
        "Cancel": "query_close"
    }

    row1 = await Button.cbutton(btn_data_row1, True)
    row2 = await Button.cbutton(btn_data_row2)

    btn = row1 + row2

    del_msg = await Message.reply_msg(update, f"\nSelect <a href='{url}'>Content</a> Quality/Format", btn=btn, disable_web_preview=False)

    timeout = 0

    while timeout < 20:
        timeout += 1
        await asyncio.sleep(1)
        localdb = await LOCAL_DATABASE.find_one("data_center", user.id)
        content_format = localdb.get("youtube_content_format")
        if content_format:
            break
    
    await Message.del_msg(chat.id, del_msg)
    await LOCAL_DATABASE.insert_data("data_center", user.id, {"youtube_content_format": None})

    if not content_format:
        await Message.reply_msg(update, "Oops, Timeout!")
        return
    
    asyncio.create_task(_func_ytdl(update, url, content_format))


async def _func_ytdl(update: Update, url, content_format):
    chat = update.effective_chat
    e_msg = update.effective_message

    sent_msg = await Message.reply_msg(update, "📥 Downloading...")
    res = await PYTUBE.ytdl(url, content_format)

    if res[0] == False:
        await Message.edit_msg(update, res[1], sent_msg)
        return
    
    await Message.edit_msg(update, "📤 Uploading...", sent_msg)

    if content_format == "mp4":
        title, file_path, thumbnail = res
        await Message.send_vid(chat.id, file_path, thumbnail, title, e_msg.id)
    elif content_format == "mp3":
        title, file_path = res
        await Message.send_audio(chat.id, file_path, title, title, e_msg.id)

    if len(res) == 3:
        rem_files = [res[1], res[2]]
    else:
        rem_files = [res[1]]
    for rem in rem_files:
        try:
            os.remove(rem)
            logger.info(f"{rem} Removed...")
        except Exception as e:
            logger.error(e)
    
    await Message.del_msg(chat.id, sent_msg)
