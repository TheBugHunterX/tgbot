import os
import requests
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.database.local_database import LOCAL_DATABASE


async def func_imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    prompt = " ".join(context.args)

    if not prompt:
        await Message.reply_msg(update, "<code>!imagine prompt</code>")
        return

    # temporarily added imagine
    imagine_api = await LOCAL_DATABASE.get_data("bot_docs", "imagine_api")
    try:
        res = requests.get(f"{imagine_api}{prompt}")
    except Exception as e:
        logger.error(e)
    
    if not res.content:
        await Message.reply_msg(update, "Try again later!")
        return
    
    os.makedirs("download", exist_ok=True)
    file_name = "download/tmp_imagine.png"
    
    with open(file_name, "wb") as f:
        f.write(res.content)

    await Message.send_img(chat.id, file_name, reply_msg_id=e_msg.id)

    try:
        os.remove(file_name)
    except Exception as e:
        logger.error(e)

    '''
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    prompt = " ".join(context.args)

    if chat.type != "private":
        db = await global_search("groups", "chat_id", chat.id)
        if db[0] == False:
            await Message.reply_msg(update, db[1])
            return
        
        find_group = db[1]
        
        ai_status = find_group.get("ai_status") or True
        if not ai_status:
            await Message.del_msg(chat.id, e_msg)
            return

    if not prompt:
        await Message.reply_msg(update, "Use <code>/imagine prompt</code>\nE.g. <code>/imagine a cute cat</code>")
        return
    
    sent_msg = await Message.reply_msg(update, "Processing...")

    imagine = await Safone.imagine(prompt)
    if not imagine or not imagine.name:
        await Message.edit_msg(update, "An error occured, try again after sometime!", sent_msg)
        return
    
    await Message.del_msg(chat.id, sent_msg)
    
    msg = f"» <i>{prompt}</i>"
    if chat.type != "private":
        msg += f"\n<b>Req by</b>: {user.mention_html()}"
    
    await Message.send_img(chat.id, imagine, msg)
    '''
