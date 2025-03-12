import os
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.modules.psndl.psndl import PSNDL

async def func_rap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_message = update.effective_message
    hex_data = " ".join(context.args)

    if not hex_data:
        await effective_message.reply_text("Use <code>/rap rap data (hex)</code>\nE.g. <code>/rap D78710F4C0979FAD9CDB40C612C94F60</code>\n<i><b>Note:</b> You will get the rap data after searching content/game using /psndl command.</i>")
        return

    await effective_message.reply_text("Creating...")

    result = PSNDL.gen_rap(hex_data)
    if not result:
        await effective_message.edit_text("RAP file wasn't found!")
        return
    
    rap_file = open(result["rap_path"], "rb").read()

    caption = (
        f"<b>• ID:</b> <code>{result['game_data'].get('id')}</code>\n"
        f"<b>• Name:</b> <code>{result['game_data'].get('name')}</code>\n"
        f"<b>• Type:</b> <code>{result['game_data'].get('type')}</code>\n"
        f"<b>• Region:</b> <code>{result['game_data'].get('region')}</code>\n"
    )

    await effective_message.reply_document(rap_file, caption, filename=result["rap_name"])
    await effective_message.delete()

    # Removing rap file from storage
    try:
        os.remove(result["rap_path"])
    except Exception as e:
        logger.error(e)
