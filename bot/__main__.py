import asyncio
import aiohttp
from time import time
from telegram import Update, LinkPreviewOptions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    PrefixHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes,
    Defaults
)
from telegram.error import BadRequest
from telegram.constants import ParseMode
from bot import ENV_CONFIG, DEFAULT_ERROR_CHANNEL_ID, bot, logger
from bot.alive import alive
from bot.update_db import update_database
from bot.helper.callbackbtn_helper import func_callbackbtn
from bot.modules.database import MemoryDB
from bot.functions.sudo_users import fetch_sudos
from bot.functions.core.start import func_start
from bot.functions.core.help import func_help
from bot.functions.filters.text_caption import func_filter_text_caption
from bot.functions.user_func.movieinfo import func_movie
from bot.functions.user_func.translator import func_tr
from bot.functions.user_func.b64decode import func_decode
from bot.functions.user_func.b64encode import func_encode
from bot.functions.user_func.shortener import func_shorturl
from bot.functions.user_func.ping import func_ping
from bot.functions.user_func.calc import func_calc
from bot.functions.user_func.text_to_speech import func_tts
from bot.functions.user_func.weather import func_weather
from bot.functions.user_func.imagine import func_imagine
from bot.functions.user_func.chatgpt import func_gpt
from bot.functions.user_func.gen_qr import func_qr
from bot.functions.user_func.img_to_link import func_imgtolink
from bot.functions.user_func.paste import func_paste
from bot.functions.user_func.ytdl import func_ytdl
from bot.functions.user_func.info import func_info
from bot.functions.user_func.psndl import func_psndl
from bot.functions.user_func.gen_rap import func_rap
from bot.functions.user_func.settings import func_settings
from bot.functions.user_func.id import func_id
from bot.functions.owner_func.broadcast import func_broadcast
from bot.functions.owner_func.send import func_send
from bot.functions.owner_func.chat_admins import func_cadmins
from bot.functions.owner_func.invitelink import func_invitelink
from bot.functions.owner_func.database import func_database
from bot.functions.owner_func.bsettings import func_bsettings
from bot.functions.owner_func.shell import func_shell
from bot.functions.owner_func.log import func_log
from bot.functions.owner_func.sys import func_sys
# from bot.functions.group_management.invite_link import func_invite_link
# from bot.functions.group_management.whisper import func_whisper
# from bot.functions.group_management.promote import (
#     func_promote,
#     func_apromote,
#     func_spromote,
#     func_sapromote,
#     func_fpromote,
#     func_fapromote,
#     func_sfpromote,
#     func_sfapromote
# )
# from bot.functions.group_management.admin_title import func_admintitle, func_sadmintitle
# from bot.functions.group_management.demote import func_demote, func_sdemote
# from bot.functions.group_management.pin_msg import func_pin_msg, func_spin_msg
# from bot.functions.group_management.unpin_msg import func_unpin_msg, func_sunpin_msg
# from bot.functions.group_management.unpinall_msg import func_unpinall_msg, func_sunpinall_msg
from bot.functions.group_management.ban import func_ban
# from bot.functions.group_management.unban import func_unban, func_sunban
# from bot.functions.group_management.kick import func_kick, func_skick
# from bot.functions.group_management.kickme import func_kickme
# from bot.functions.group_management.mute import func_mute, func_smute
# from bot.functions.group_management.unmute import func_unmute, func_sunmute
# from bot.functions.group_management.del_msg import func_del, func_sdel
# from bot.functions.group_management.purge import func_purge, func_spurge, func_purgefrom, func_purgeto
# from bot.functions.group_management.lock_chat import func_lockchat
# from bot.functions.group_management.unlock_chat import func_unlockchat
# from bot.functions.group_management.add_filter import func_filter
# from bot.functions.group_management.remove_filter import func_remove
# from bot.functions.group_management.filters import func_filters
# from bot.functions.group_management.adminlist import func_adminlist
# from bot.functions.group_management.track_bot_chat import track_bot_chat_act
# from bot.functions.group_management.track_other_chat import track_other_chat_act


async def post_boot():
    # storing bot uptime
    MemoryDB.insert_data("bot_data", None, {"bot_uptime": str(time())})
    # deleting bot commands set
    try:
        await bot.delete_my_commands()
    except Exception as e:
        logger.error(e)

    # Send alive message to all sudo and bot owner
    sudo_users = fetch_sudos()

    try:
        await asyncio.gather(*(bot.send_message(user_id, "<b>Bot Started!</b>", parse_mode=ParseMode.HTML) for user_id in sudo_users))
    except Exception as e:
        logger.error(e)


async def server_alive():
    # executing after updating database so getting data from memory...
    server_url = MemoryDB.bot_data.get("server_url")
    if not server_url:
        logger.warning("⚠️ Server url not provided !!")
        await bot.send_message(ENV_CONFIG["owner_id"], "⚠️ Server url not provided!\nGoto /bsettings and setup server url then restart bot...")
        return
    
    while True:
        # everytime check if there is new server_url
        server_url = MemoryDB.bot_data.get("server_url")
        if not server_url:
            return
        if server_url[0:4] != "http":
            server_url = f"http://{server_url}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(server_url) as response:
                    if response.status != 200:
                        logger.warning(f"{server_url} is down or unreachable. ❌ - code - {response.status_code}")
        except Exception as e:
            logger.error(f"{server_url} > {e}")
        await asyncio.sleep(180) # 3 min


async def default_error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(context.error)

    if update:
        user = update.effective_user
        chat = update.effective_chat
        effective_message = update.effective_message
        query = update.callback_query
        query_data = query.data if query else None
        chat_title = chat.full_name or chat.title

        text = (
            "<b>⚠️ An error occured: [/log]</b>\n\n"
            f"<b>User:</b> {user.mention_html()} | <code>{user.id}</code>\n"
            f"<b>Chat:</b> {chat_title} | <code>{chat.id}</code>\n"
            f"<b>Effective message:</b> <code>{effective_message.text}</code>\n"
            f"<b>Query message:</b> <code>{query_data}</code>\n\n"
            f"<pre>{context.error}</pre>"
        )
    else:
        text = (
            "<b>⚠️ An error occured: [/log]</b>\n\n"
            f"<pre>{context.error}</pre>"
        )

    try:
        await context.bot.send_message(DEFAULT_ERROR_CHANNEL_ID, text)
    except BadRequest:
        await context.bot.send_message(ENV_CONFIG["owner_id"], text)
    except Exception as e:
        logger.error(e)


def main():
    default_param = Defaults(
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        block=False,
        allow_sending_without_reply=True
    )
    # Bot instance
    application = ApplicationBuilder().token(ENV_CONFIG["bot_token"]).defaults(default_param).build()
    # functions
    BOT_COMMANDS = {
        "start": func_start,
        "movie": func_movie,
        "tr": func_tr,
        "decode": func_decode,
        "encode": func_encode,
        "shorturl": func_shorturl,
        "ping": func_ping,
        "calc": func_calc,
        "tts": func_tts,
        "weather": func_weather,
        "imagine": func_imagine,
        "gpt": func_gpt,
        "qr": func_qr,
        "imgtolink": func_imgtolink,
        "paste": func_paste,
        # "whisper": func_whisper,
        "ytdl": func_ytdl,
        "info": func_info,
        "psndl": func_psndl,
        "rap": func_rap,
        "settings": func_settings,
        # Group management
        "id": func_id,
        # "invite": func_invite_link,
        # "promote": func_promote,
        # "apromote": func_apromote,
        # "spromote": func_spromote,
        # "sapromote": func_sapromote,
        # "fpromote": func_fpromote,
        # "fapromote": func_fapromote,
        # "sfpromote": func_sfpromote,
        # "sfapromote": func_sfapromote,
        # "admintitle": func_admintitle,
        # "sadmintitle": func_sadmintitle,
        # "demote": func_demote,
        # "sdemote": func_sdemote,
        # "pin": func_pin_msg,
        # "spin": func_spin_msg,
        # "unpin": func_unpin_msg,
        # "sunpin": func_sunpin_msg,
        # "unpinall": func_unpinall_msg,
        # "sunpinall": func_sunpinall_msg,
        "ban": func_ban,
        # "sban": func_sban,
        # "unban": func_unban,
        # "sunban": func_sunban,
        # "kick": func_kick,
        # "skick": func_skick,
        # "kickme": func_kickme,
        # "mute": func_mute,
        # "smute": func_smute,
        # "unmute": func_unmute,
        # "sunmute": func_sunmute,
        # "del": func_del,
        # "sdel": func_sdel,
        # "purge": func_purge,
        # "spurge": func_spurge,
        # "purgefrom": func_purgefrom,
        # "purgeto": func_purgeto,
        # "lock": func_lockchat,
        # "unlock": func_unlockchat,
        # "filter": func_filter,
        # "remove": func_remove,
        # "filters": func_filters,
        # "adminlist": func_adminlist,
        "help": func_help,
        # owner commands...
        "broadcast": func_broadcast,
        "send": func_send,
        "cadmins": func_cadmins,
        "invitelink": func_invitelink,
        "database": func_database,
        "bsettings": func_bsettings,
        "shell": func_shell,
        "log": func_log,
        "sys": func_sys
    }

    storage = []
    for command, handler in BOT_COMMANDS.items():
        storage.append(f"/{command}")
        application.add_handler(CommandHandler(command, handler)) # for /command
        application.add_handler(PrefixHandler(["!", ".", "-"], command, handler)) # for other prefix command
    
    # storing bot commands
    MemoryDB.insert_data("bot_data", None, {"bot_commands": storage})
    
    # filters
    # application.add_handler(MessageHandler(filters.COMMAND, func_del_command))
    application.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, func_filter_text_caption))
    # Chat Member Handler
    # application.add_handler(ChatMemberHandler(track_bot_chat_act, ChatMemberHandler.MY_CHAT_MEMBER)) # for tacking bot/private chat
    # application.add_handler(ChatMemberHandler(track_other_chat_act, ChatMemberHandler.CHAT_MEMBER)) # for tacking group/supergroup/channel
    # Callback button
    application.add_handler(CallbackQueryHandler(func_callbackbtn))
    # Error handler
    application.add_error_handler(default_error_handler)
    # Check Updates
    application.run_polling(allowed_updates=Update.ALL_TYPES)


async def start_up_work():
    alive() # Server breathing
    update_database()
    await post_boot()
    await server_alive()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(start_up_work())
    loop.create_task(main())
    loop.run_forever()
