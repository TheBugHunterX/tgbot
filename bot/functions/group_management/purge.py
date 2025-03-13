import asyncio
from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType


from bot.modules.database import MemoryDB
from bot.functions.group_management.pm_error import _pm_error
from bot.functions.group_management.log_channel import _log_channel

from bot.functions.group_management.check_permission import _check_permission


async def func_purge(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None, purgefrom_id=None):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    reply = update.message.reply_to_message
    
    if chat.type == ChatType.PRIVATE:
        await _pm_error(chat.id)
        return

    

    if user.is_bot:
        await effective_message.reply_text("I don't take permission from anonymous admins!")
        return
    
    sent_message = await effective_message.reply_text("💭")
    _chk_per = await _check_permission(update, user=user)
    if not _chk_per:
        await Message.edit_message(update, "Oops! Something went wrong!", sent_msg)
        return
    
    if _chk_per["bot_permission"].status != ChatMember.ADMINISTRATOR:
        await Message.edit_message(update, "I'm not an admin in this chat!", sent_msg)
        return
    
    if _chk_per["user_permission"].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.edit_message(update, "You aren't an admin in this chat!", sent_msg)
        return
    
    if _chk_per["user_permission"].status == ChatMember.ADMINISTRATOR:
        if not _chk_per["user_permission"].can_delete_messages:
            await Message.edit_message(update, "You don't have enough rights to delete chat messages!", sent_msg)
            return
    
    if not _chk_per["bot_permission"].can_delete_messages:
        await Message.edit_message(update, "I don't have enough rights to delete chat messages!", sent_msg)
        return
    
    if not reply:
        await Message.edit_message(update, "I don't know which message to delete from! Reply the message that you want to start delete from!\n\n<i><b>Note:</b> bots are unable to delete 48h old messages due to Telegram limitation/restriction...</i>", sent_msg)
        return
    
    await Message.edit_message(update, f"🚀 Purge started...", sent_msg)

    if purgefrom_id:
        while purgefrom_id <= reply.id:
            await Message.delete_message(chat.id, purgefrom_id)
            purgefrom_id += 1
    else:
        await asyncio.gather(*(Message.delete_message(chat.id, msg_id) for msg_id in range(reply.id, e_msg.id + 1)))

    if is_silent:
        await Message.delete_message(chat.id, sent_msg)
    else:
        await Message.edit_message(update, f"✅ Purge completed!", sent_msg)
    await _log_channel(update, chat, user, action="MSG_PURGE")


async def func_spurge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_purge(update, context, is_silent=True)


async def func_purgefrom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    reply = update.message.reply_to_message
    effective_message = update.effective_message

    if chat.type == ChatType.PRIVATE:
        await _pm_error(chat.id)
        return

    if not reply:
        await effective_message.reply_text("Reply the message with /purgefrom which message you want to purge from! Then reply the message with /purgeto where to stop purge!")
        return
    
    MemoryDB.insert_data("data_center", chat.id, {"purgefrom_id": reply.id})
    sent_message = await effective_message.reply_text("<code>purgefrom</code> added...")
    await asyncio.sleep(5)
    await Message.delete_messages(chat.id, [e_msg.id, sent_msg.id])


async def func_purgeto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type == ChatType.PRIVATE:
        await _pm_error(chat.id)
        return

    purgefrom_id = None
    data_center = MemoryDB.data_center.get(chat.id)
    if data_center:
        purgefrom_id = data_center.get("purgefrom_id")
    
    if not purgefrom_id:
        await effective_message.reply_text("Reply the message with /purgefrom which message you want to purge from! Then reply the message with /purgeto where to stop purge!")
        return
    
    MemoryDB.insert_data("data_center", chat.id, {"purgefrom_id": None})
    await func_purge(update, context, purgefrom_id=purgefrom_id)
    await asyncio.sleep(5)
    await Message.delete_message(chat.id, e_msg)
