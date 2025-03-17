from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from bot.modules.database import MemoryDB, MongoDB
from bot.modules.database.common import database_search
from bot.functions.group_management.auxiliary.pm_error import pm_error
from bot.functions.group_management.auxiliary.fetch_chat_admins import fetch_chat_admins

async def func_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    keyword = " ".join(context.args).lower()
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if user.is_bot:
        await effective_message.reply_text("Who are you? I don't take commands from anonymous admins...!")
        return
    
    chat_admins = await fetch_chat_admins(chat, user_id=user.id)
    
    if not (chat_admins["is_user_admin"] or chat_admins["is_user_owner"]):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if chat_admins["is_user_admin"] and not chat_admins["is_user_admin"].can_change_info:
        await effective_message.reply_text("You don't have enough permission to manage this chat!")
        return
    
    if not keyword:
        text = (
            "To remove an existing filter use <code>/remove keyword</code>\n"
            "Use <code>clear_all</code> instead of keyword, to delete all filters of this chat!"
        )
        await effective_message.reply_text(text)
        return

    response, database_data = database_search("groups", "chat_id", chat.id)
    if response == False:
        await effective_message.reply_text(database_data)
        return
    
    filters = database_data.get("filters")

    if filters and keyword:
        if keyword == "clear_all":
            MongoDB.update_db("groups", "chat_id", chat.id, "filters", None)
            group_data = MongoDB.find_one("groups", "chat_id", chat.id)
            MemoryDB.insert_data("chat_data", chat.id, group_data)

            await effective_message.reply_text("All filters of this chat has been removed!")
            return
        
        try:
            if keyword.lower() in filters:
                del filters[keyword]
                MongoDB.update_db("groups", "chat_id", chat.id, "filters", filters)
                await effective_message.reply_text(f"Filter <code>{keyword}</code> has been removed!")
            
            else:
                await effective_message.reply_text("Filter doesn't exist! Chat filters /filters")
                return
            
            group_data = MongoDB.find_one("groups", "chat_id", chat.id)
            MemoryDB.insert_data("chat_data", chat.id, group_data)
        except Exception as e:
            logger.error(e)
            await effective_message.reply_text(str(e))
