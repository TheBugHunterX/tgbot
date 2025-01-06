from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.group_management.log_channel import _log_channel
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_unpinall_msg(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await func_del_command(update, context)

    if user.is_bot:
        await Message.reply_message(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, victim_permission = _chk_per
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_message(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status != ChatMember.OWNER:
        await Message.reply_message(update, "This command is only for group owner!")
        return
    
    if not bot_permission.can_pin_messages:
        await Message.reply_message(update, "I don't have enough rights to pin/unpin messages!")
        return
    
    try:
        await bot.unpin_all_chat_messages(chat.id)
    except Exception as e:
        logger.error(e)
        error_msg = await Message.reply_message(update, e)
        if not error_msg:
            await Message.reply_message(update, e.message)
        return
    
    if not is_silent:
        await Message.reply_message(update, f"All message unpinned!")
    await _log_channel(update, chat, user, action="UNPIN_ALL_MSG")


async def func_sunpinall_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_unpinall_msg(update, context, is_silent=True)
