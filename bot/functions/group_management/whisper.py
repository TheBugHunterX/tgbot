from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes
from bot.modules.database import MemoryDB
from bot.functions.group_management.auxiliary_func.pm_error import _pm_error


async def func_whisper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    msg = " ".join(context.args)

    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if not msg:
        await effective_message.reply_text("Use <code>/whisper @mention_user message</code>\nor reply user by <code>/whisper message</code>\nE.g. <code>/whisper @bishalqx980 This is a secret message 😜</code>")
        return
    
    await Message.delete_message(chat.id, e_msg)

    if re_msg:
        if re_msg.from_user.is_bot:
            await effective_message.reply_text("Whisper isn't for bots...!")
            return
        whisper_user = re_msg.from_user.id
    elif msg:
        msg_split = msg.split()
        whisper_user = msg_split[0]
        msg = " ".join(msg_split[1:])

        if not whisper_user.startswith("@"):
            await effective_message.reply_text(f"Give a valid username! <code>{whisper_user}</code> is an invalid username!\nor try to reply the user. /whisper for more details...")
            return
        
        # there is a problem > anonymous admin cant read this ...
        if whisper_user.endswith("bot"):
            await effective_message.reply_text("Whisper isn't for bots...!")
            return
    
    if len(msg) > 100:
        await effective_message.reply_text("Whisper is too long... (max limit 100 character)")
        return

    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "groups",
        "db_find": "chat_id",
        "db_vlaue": chat.id,
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": e_msg.id,
        "edit_data_value_msg_pointer_id": None
    }

    MemoryDB.insert_data("data_center", chat.id, data)

    data_center = MemoryDB.data_center.get(chat.id)
    if data_center:
        whisper_data = data.get("whisper_data")
        if whisper_data:
            user_whisper_data = whisper_data.get(whisper_user)
            if user_whisper_data:
                await Message.delete_message(chat.id, user_whisper_data.get("msg_id"))
    
    data = {
        whisper_user: {
            "whisper_user": whisper_user,
            "whisper_msg": f"{user.first_name}: {msg}",
            "msg_id": e_msg.id + 1
        }
    }
    
    if data_center:
        whisper_data = data_center.get("whisper_data")
        if whisper_data:
            whisper_data.update(data)
    else:
        MemoryDB.insert_data("data_center", chat.id, {"whisper_data": data})

    if re_msg:
        whisper_user = re_msg.from_user.mention_html()

    btn = ButtonMaker.cbutton([{"Check the message 👀": "query_whisper"}])
    await effective_message.reply_text(f"Hey, {whisper_user} !! You got a message from {user.mention_html()}...", reply_markup=btn)
