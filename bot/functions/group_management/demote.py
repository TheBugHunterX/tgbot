from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from bot.functions.group_management.auxiliary.pm_error import pm_error
from bot.functions.group_management.auxiliary.fetch_chat_admins import fetch_chat_admins

async def func_demote(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    victim = re_msg.from_user if re_msg else None
    reason = " ".join(context.args)

    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return

    if user.is_bot:
        await effective_message.reply_text("Who are you? I don't take commands from anonymous admins...!")
        return
    
    if not re_msg:
        await effective_message.reply_text("I don't know who you are talking about! Reply the member whom you want to demote!\nE.g<code>/demote reason</code>")
        return
    
    if victim.id == context.bot.id:
        await effective_message.reply_text("I'm not going to demote myself!")
        return
    
    chat_admins = await fetch_chat_admins(chat, context.bot.id, user.id, victim.id)
    
    if not (chat_admins["is_user_admin"] or chat_admins["is_user_owner"]):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return

    if chat_admins["is_victim_owner"]:
        await effective_message.reply_text("I'm not going to demote chat owner! You must be kidding!")
        return
    
    if chat_admins["is_user_admin"] and not chat_admins["is_user_admin"].can_promote_members:
        await effective_message.reply_text("You don't have enough permission to demote chat members!")
        return
    
    if not chat_admins["is_bot_admin"]:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    if not chat_admins["is_bot_admin"].can_promote_members:
        await effective_message.reply_text("I don't have enough permission to demote chat members!")
        return
    
    try:
        await chat.promote_member(victim.id)
    except Exception as e:
        logger.error(e)
        await effective_message.reply_text(str(e))
        return
    
    if not is_silent:
        text = f"{victim.mention_html()} has been demoted." + (f"\nReason: {reason}" if reason else "")
        await effective_message.reply_text(text)


async def func_sdemote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.effective_message.delete()
    await func_demote(update, context, is_silent=True)
