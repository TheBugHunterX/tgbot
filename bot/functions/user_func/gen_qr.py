import os
from time import time
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.modules.qr import QR

async def func_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    data = " ".join(context.args) or (re_msg.text or re_msg.caption if re_msg else None)

    if not data:
        await effective_message.reply_text("Use <code>/qr url/data/text</code> to generate a QR code.\nor reply the 'url/data/text' with <code>/qr</code> command.\nE.g. <code>/qr https://google.com</code>")
        return

    await effective_message.reply_text(f"💭 Generating...")
    start_time = time()
    response = QR.generate_qr(data, f"qrcode_{user.id}")
    response_time = int((time() - start_time) * 1000) # conveting into ms

    if not response:
        await effective_message.edit_text("Oops! Something went wrong!")
        return
    
    caption = (
        f"<b>💭 Data:</b> <code>{data}</code>\n"
        f"<b>⏳ R.time:</b> <code>{response_time}ms</code>\n"
        f"<b>🗣 Req by:</b> {user.mention_html()} | <code>{user.id}</code>"
    )
    
    reply_message_id = re_msg.id if re_msg else effective_message.id
    await effective_message.reply_photo(response, caption, reply_to_message_id=reply_message_id)
    await effective_message.delete()

    # Remove the image from storage
    try:
        os.remove(response)
    except Exception as e:
        logger.error(e)
