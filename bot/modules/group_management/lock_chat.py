from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.group_management.log_channel import _log_channel
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_lockchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_message(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not user_permission.can_change_info:
            await Message.reply_message(update, "You don't have enough rights to manage this chat!")
            return
    
    if not bot_permission.can_change_info:
        await Message.reply_message(update, "I don't have enough rights to manage this chat!")
        return
    
    permissions = {
        "can_send_messages": False,
        "can_send_other_messages": False,
        "can_add_web_page_previews": False,
        "can_send_audios": False,
        "can_send_documents": False,
        "can_send_photos": False,
        "can_send_videos": False,
        "can_send_video_notes": False,
        "can_send_voice_notes": False,
        "can_send_polls": False
    }

    try:
        await bot.set_chat_permissions(chat.id, permissions)
    except Exception as e:
        logger.error(e)
        await Message.reply_message(update, str(e))
        return

    await Message.send_message(chat.id, f"This chat has been locked!\n<b>Admin:</b> {user.first_name}")
    await _log_channel(update, chat, user, action="CHAT_LOCK")
