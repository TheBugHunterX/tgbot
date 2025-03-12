import psutil
from time import time
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB, MongoDB

class QueryBotHelp:
    async def _query_help_group_management_p1(update: Update):
        effective_message = update.effective_message

        text = (
            "<b>Group Moderation Commands | p:1</b>\n\n"
            "/id » Show chat/user id\n"
            "/invite » Generate chat invite link\n"
            "/promote | /fpromote » promote a member ('f' means with full privilege)\n"
            "/apromote | /fapromote » <code>anonymously</code> promote/fpromote a member\n"
            "/admintitle » set admin custom title\n"
            "/demote » demote a member\n"
            "/pin » pin replied message loudly\n"
            "/unpin » unpin a pinned message\n"
            "/unpinall » unpin all pinned messages"
            "/ban » ban a member\n"
            "/unban » unban a member\n"
            "/kick » kick a member\n"
            "/kickme » The easy way to out\n"
            "/mute » restrict a member (member will be unable to send messages etc.)\n"
            "/unmute » unrestrict a restricted member\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!\n"
            "Some command has a silent function! eg. <code>/s[command]</code> » /sban etc.</i>"
        )

        btn_data = [
            {"Next page →": "query_help_group_management_p2"},
            {"Back": "query_help_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_help_group_management_p2(update: Update):
        effective_message = update.effective_message

        text = (
            "<b>Group Moderation Commands | p:2</b>\n\n"
            "/del » delete the replied message with a warning!\n"
            "/purge » delete every messages from replied to current message!\n"
            "/purgefrom | /purgeto » delete every messages between <code>purgefrom</code> and <code>purgeto</code> replied message!\n"
            "/lock » lock the chat (member will be unable to send messages etc.)\n"
            "/unlock » unlock the chat (back to normal)\n"
            "/filters | /filter | /remove » to see/set/remove custom message/command\n"
            "/adminlist » to see chat admins list\n"
            "/settings » settings of chat\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!\n"
            "Some command has a silent function! eg. <code>/s[command]</code> » /sban etc.</i>"
        )

        btn_data = [
            {"← Previous page": "query_help_group_management_p1"},
            {"Back": "query_help_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_help_ai(update: Update):
        effective_message = update.effective_message

        text = (
            "<b>Artificial intelligence</b>\n\n"
            "/imagine » generate AI image\n"
            "/gpt » ask any question to ChatGPT\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )

        btn = ButtonMaker.cbutton([{"Back": "query_help_menu", "Close": "query_close"}])

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_help_misc_functions(update: Update):
        effective_message = update.effective_message

        text = (
            "<b>Misc functions</b>\n\n"
            "/movie » get any movie info by name or imdb id\n"
            "/tr » translate any language\n"
            "/decode » convert base64 into text\n"
            "/encode » convert text into base64\n"
            "/shorturl » short any url\n"
            "/ping » ping any url\n"
            "/calc » calculate any math (supported syntex: +, -, *, /)\n"
            "/tts » convert text into speech\n"
            "/weather » get weather info of any city\n"
            "/qr » generate a QR code\n"
            "/imgtolink » convert image into a public link\n"
            "/paste » paste your text in telegraph & get public link\n"
            "/whisper » secretly tell something to someone in group chat\n"
            "/ytdl » download audio/song from youtube\n"
            "/id » show chat/user id\n"
            "/info » show user info\n"
            "/psndl » search ps3 & some other playstation games link (mostly ps3)\n"
            "/rap » generate rap from <code>rap_data</code> (use /psndl to get rap data)\n"
            "/settings » settings of chat\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )
        
        btn = ButtonMaker.cbutton([{"Back": "query_help_menu", "Close": "query_close"}])

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_help_owner_functions(update: Update):
        effective_message = update.effective_message

        text = (
            "<b>Bot owner functions</b>\n\n"
            "/broadcast » broadcast message to all active users\n"
            "/send » send message to specified chat_id\n"
            "/chatadmins » to get adminlist of specified chat_id\n"
            "/invitelink » to get invite link of specified chat_id\n"
            "/database » get bot/chat database\n"
            "/bsettings » get bot settings\n"
            "/shell » use system shell\n"
            "/log » get log file (for error handling)\n"
            "/sys » get system info\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )
        
        btn = ButtonMaker.cbutton([{"Back": "query_help_menu", "Close": "query_close"}])

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)
    

    async def _query_help_bot_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
        effective_message = update.effective_message

        database_info = MongoDB.info_db()
        total_users = None
        total_groups = None

        for info in database_info:
            info = database_info[info]
            if info.get("name") == "users":
                total_users = info.get("quantity")
            elif info.get("name") == "groups":
                total_groups = info.get("quantity")
            
            if total_users and total_groups:
                break
        
        active_status = MongoDB.find("users", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)

        sys_uptime = timedelta(seconds=datetime.now().timestamp() - psutil.boot_time())

        sys_days = sys_uptime.days
        sys_hours, remainder = divmod(sys_uptime.seconds, 3600)
        sys_minute = remainder / 60

        bot_uptime = timedelta(seconds=time() - float(MemoryDB.bot_data.get("bot_uptime", 0)))

        bot_days = bot_uptime.days
        bot_hours, remainder = divmod(bot_uptime.seconds, 3600)
        bot_minute = remainder / 60

        bot_commands = MemoryDB.bot_data.get("bot_commands", [])

        text = (
            "<blockquote><code><b>» bot.info()</b></code></blockquote>\n\n"

            f"<b>• Name:</b> {context.bot.first_name}\n"
            f"<b>• ID:</b> <code>{context.bot.id}</code>\n"
            f"<b>• Username:</b> {context.bot.name}\n\n"

            f"<b>• Registered users:</b> <code>{total_users}</code>\n"
            f"<b>• Active users:</b> <code>{active_users}</code>\n"
            f"<b>• Inactive users:</b> <code>{inactive_users}</code>\n"
            f"<b>• Total chats:</b> <code>{total_groups}</code>\n\n"

            f"<b>• System uptime:</b> <code>{int(sys_days)}d {int(sys_hours)}h {int(sys_minute)}m</code>\n"
            f"<b>• Bot uptime:</b> <code>{int(bot_days)}d {int(bot_hours)}h {int(bot_minute)}m</code>\n"
            f"<b>• Total commands:</b> <code>{len(bot_commands)}</code>\n\n"

            "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
            "<b>• Report bug:</b> <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
            "<b>• Developer:</b> <a href='https://t.me/bishalqx980'>bishalqx980</a>"
        )
        
        btn = ButtonMaker.cbutton([{"Back": "query_help_menu", "Close": "query_close"}])

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)
