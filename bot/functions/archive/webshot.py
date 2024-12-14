from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.safone import Safone

async def func_webshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    url = " ".join(context.args)

    if not url:
        await Message.reply_msg(update, "Use <code>/webshot url</code>\nE.g. <code>/webshot https://google.com</code>")
        return
    
    if url[0:4] != "http":
        url = f"http://{url}"

    sent_msg = await Message.reply_msg(update, "Taking webshot please wait...")
    webshot = await Safone.webshot(url)
    if webshot:
        await Message.del_msg(chat.id, sent_msg)
        await Message.send_img(chat.id, webshot, f"⇾ {url}")
    else:
        await Message.edit_msg(update, "Oops, something went wrong...", sent_msg)
