from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from bot.functions.group_management.auxiliary.pm_error import pm_error
from bot.functions.group_management.auxiliary.fetch_chat_admins import fetch_chat_admins

async def func_kickme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    chat_admins = await fetch_chat_admins(chat, context.bot.id, user.id)
    
    if (chat_admins["is_user_admin"] or chat_admins["is_user_owner"]):
        await effective_message.reply_text("I'm not going to kick you! You must be kidding!")
        return
    
    if not chat_admins["is_bot_admin"]:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    if not chat_admins["is_bot_admin"].can_restrict_members:
        await effective_message.reply_text("I don't have enough permission to kick members in this chat!")
        return
    
    try:
        await chat.unban_member(user.id)
    except Exception as e:
        logger.error(e)
        await effective_message.reply_text(str(e))
        return
    
    await effective_message.reply_text(f"Nice Choice! Get out of my sight!\n{user.mention_html()} has chosen the easy way to out!")
