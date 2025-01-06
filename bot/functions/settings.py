import random
from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import global_search
from bot.modules.database.combined_db import find_bot_docs
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    _bot = await find_bot_docs()
    if not _bot:
        return

    if chat.type == "private":
        data = {
            "user_id": user.id,
            "chat_id": chat.id,
            "collection_name": "users",
            "db_find": "user_id",
            "db_vlaue": user.id,
            "edit_data_key": None,
            "edit_data_value": None,
            "del_msg_pointer_id": e_msg.id,
            "edit_data_value_msg_pointer_id": None
        }

        await LOCAL_DATABASE.insert_data("data_center", chat.id, data)

        db = await global_search("users", "user_id", user.id)
        if db[0] == False:
            await Message.reply_message(update, db[1])
            return
        
        find_user = db[1]
        
        user_mention = find_user.get("mention")
        lang = find_user.get("lang")
        echo = find_user.get("echo")
        auto_tr = find_user.get("auto_tr")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"• User: {user_mention}\n"
            f"• ID: <code>{chat.id}</code>\n\n"

            f"• Lang: <code>{lang}</code>\n"
            f"• Echo: <code>{echo}</code>\n"
            f"• Auto tr: <code>{auto_tr}</code>\n\n"
        )

        btn_data_row1 = {
            "Language": "query_chat_lang",
            "Auto translate": "query_chat_auto_tr"
        }

        btn_data_row2 = {
            "Echo": "query_chat_set_echo",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1, True)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        _bot = await find_bot_docs()
        if not _bot:
            return
        
        images = _bot.get("images")
        if images:
            image = random.choice(images).strip()
        else:
            image = _bot.get("bot_pic")

        if image:
            await Message.send_image(chat.id, image, msg, btn=btn)
        else:
            await Message.send_message(chat.id, msg, btn=btn)

    elif chat.type in ["group", "supergroup"]:
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
        
        await LOCAL_DATABASE.insert_data("data_center", chat.id, data)

        db = await global_search("groups", "chat_id", chat.id)
        if db[0] == False:
            await Message.reply_message(update, db[1])
            return
        
        find_group = db[1]
        
        title = find_group.get("title")
        lang = find_group.get("lang")
        echo = find_group.get("echo")
        auto_tr = find_group.get("auto_tr")
        welcome_user = find_group.get("welcome_user")
        farewell_user = find_group.get("farewell_user")
        antibot = find_group.get("antibot")
        ai_status = find_group.get("ai_status") or True
        del_cmd = find_group.get("del_cmd")
        all_links = find_group.get("all_links")
        allowed_links = find_group.get("allowed_links")
        log_channel = find_group.get("log_channel")
        
        if allowed_links:
            storage, counter = "", 0
            for i in allowed_links:
                counter += 1
                if counter == len(allowed_links):
                    storage += f"{i}"
                else:
                    storage += f"{i}, "
            allowed_links = storage

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"• Title: {title}\n"
            f"• ID: <code>{chat.id}</code>\n\n"

            f"• Lang: <code>{lang}</code>\n"
            f"• Auto tr: <code>{auto_tr}</code>\n"
            f"• Echo: <code>{echo}</code>\n"
            f"• Antibot: <code>{antibot}</code>\n"
            f"• Welcome user: <code>{welcome_user}</code>\n"
            f"• Farewell user: <code>{farewell_user}</code>\n"
            f"• Delete CMD: <code>{del_cmd}</code>\n"
            f"• Log channel: <code>{log_channel}</code>\n"
            f"• All links: <code>{all_links}</code>\n"
            f"• Allowed links: <code>{allowed_links}</code>\n"
            f"• AI status: <code>{ai_status}</code>\n"
        )

        btn_data_row1 = {
            "Language": "query_chat_lang",
            "Auto translate": "query_chat_auto_tr"
        }

        btn_data_row2 = {
            "Echo": "query_chat_set_echo",
            "Anti bot": "query_chat_antibot"
        }

        btn_data_row3 = {
            "Welcome": "query_chat_welcome_user",
            "Farewell": "query_chat_farewell_user"
        }

        btn_data_row4 = {
            "Delete CMD": "query_chat_del_cmd",
            "Log channel": "query_chat_log_channel"
        }

        btn_data_row5 = {
            "Links behave": "query_chat_links_behave",
            "AI status": "query_chat_ai_status"
        }

        btn_data_row6 = {
            "Close": "query_close"
        }

        row2 = await Button.cbutton(btn_data_row2, True)
        row3 = await Button.cbutton(btn_data_row3, True)
        row1 = await Button.cbutton(btn_data_row1, True)
        row4 = await Button.cbutton(btn_data_row4, True)
        row5 = await Button.cbutton(btn_data_row5, True)
        row6 = await Button.cbutton(btn_data_row6)

        btn = row1 + row2 + row3 + row4 + row5 + row6

        _bot = await find_bot_docs()
        if not _bot:
            return
        
        images = _bot.get("images")
        if images:
            image = random.choice(images).strip()
        else:
            image = _bot.get("bot_pic")
        
        if image:
            await Message.send_image(chat.id, image, msg, btn=btn)
        else:
            await Message.send_message(chat.id, msg, btn=btn)
