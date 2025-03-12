from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.telegraph import TELEGRAPH

async def func_paste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    text = (re_msg.text_html or re_msg.caption_html) if re_msg else " ".join(context.args)

    if not text:
        await effective_message.reply_text("Use <code>/paste text</code> or reply the message/text with <code>/paste</code> command.")
        return

    await effective_message.reply_text(f"Creating...")
    paste = TELEGRAPH.paste(text.replace("\n", "<br>"), user.full_name)
    if not paste:
        await effective_message.edit_text("Oops! Something went wrong!")
        return
    
    await effective_message.edit_text(paste)
