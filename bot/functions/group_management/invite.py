from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from bot.functions.group_management.auxiliary.pm_error import pm_error
from bot.functions.group_management.auxiliary.fetch_chat_admins import fetch_chat_admins

async def func_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if chat.link:
        await effective_message.reply_text(f"Invite link: {chat.link}")
        return
    
    if user.is_bot:
        await effective_message.reply_text("Who are you? I don't take commands from anonymous admins...!")
        return
    
    chat_admins = await fetch_chat_admins(chat, context.bot.id, user.id)
    
    if not (chat_admins["is_user_admin"] or chat_admins["is_user_owner"]):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if chat_admins["is_user_admin"] and not chat_admins["is_user_admin"].can_invite_users:
        await effective_message.reply_text("You don't have enough permission to invite members in this chat!")
        return
    
    if not chat_admins["is_bot_admin"]:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    if not chat_admins["is_bot_admin"].can_invite_users:
        await effective_message.reply_text("I don't have enough permission to invite members in this chat!")
        return
    
    try:
        invite_link = await chat.create_invite_link(name=user.full_name)
    except Exception as e:
        logger.error(e)
        await effective_message.reply_text(str(e))
        return
    
    await effective_message.reply_text(f"Invite link: {invite_link.invite_link}")
