from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType


from bot.functions.group_management.pm_error import _pm_error
from bot.functions.group_management.log_channel import _log_channel

from bot.functions.group_management.check_permission import _check_permission


async def func_del(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    reason = " ".join(context.args)

    if chat.type == ChatType.PRIVATE:
        await _pm_error(chat.id)
        return

    

    if user.is_bot:
        await effective_message.reply_text("I don't take permission from anonymous admins!")
        return
    
    sent_msg = await effective_message.reply_text("💭")
    _chk_per = await _check_permission(update, victim, user)
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
        await Message.edit_message(update, "I don't know which message to delete! Reply the message that you want to delete!\nTo mention with reason eg. <code>/del reason</code>", sent_msg)
        return

    await Message.delete_messages(chat.id, [e_msg.id, reply.id])
    
    if is_silent:
        await Message.delete_message(chat.id, sent_msg)
    else:
        msg = f"Lookout... {victim.mention_html()}, your message has been deleted!\n<b>Admin:</b> {user.first_name}"
        if reason:
            msg = f"{msg}\n<b>Reason</b>: {reason}"
        
        await Message.edit_message(update, msg, sent_msg)
    
    await _log_channel(update, chat, user, victim, action="MSG_DEL", reason=reason)


async def func_sdel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_del(update, context, is_silent=True)
