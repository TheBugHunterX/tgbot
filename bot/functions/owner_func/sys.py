import psutil
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users


async def func_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "Access denied!")
        return
    
    sys_info = (
        f"<b>↺ System info</b>\n\n"
        f"<b>• <u>CPU</u></b>\n"
        f"<b>CPU:</b> <code>{psutil.cpu_count()}</code>\n"
        f"<b>CPU (Logical):</b> <code>{psutil.cpu_count(False)}</code>\n"
        f"<b>CPU freq Current:</b> <code>{psutil.cpu_freq()[0]/1024:.2f} Ghz</code>\n"
        f"<b>CPU freq Max:</b> <code>{psutil.cpu_freq()[2]/1024:.2f} Ghz</code>\n\n"
        f"<b>• <u>RAM</u></b>\n"
        f"<b>RAM Total:</b> <code>{psutil.virtual_memory()[0]/(1024**3):.2f} GB</code>\n"
        f"<b>RAM Avail:</b> <code>{psutil.virtual_memory()[1]/(1024**3):.2f} GB</code>\n"
        f"<b>RAM Used:</b> <code>{psutil.virtual_memory()[3]/(1024**3):.2f} GB</code>\n"
        f"<b>RAM Free:</b> <code>{psutil.virtual_memory()[4]/(1024**3):.2f} GB</code>\n"
        f"<b>RAM Percent:</b> <code>{psutil.virtual_memory()[2]} %</code>\n\n"
        f"<b>• <u>RAM (Swap)</u></b>\n"
        f"<b>RAM Total (Swap):</b> <code>{psutil.swap_memory()[0]/(1024**3):.2f} GB</code>\n"
        f"<b>RAM Used (Swap):</b> <code>{psutil.swap_memory()[1]/(1024**3):.2f} GB</code>\n"
        f"<b>RAM Free (Swap):</b> <code>{psutil.swap_memory()[2]/(1024**3):.2f} GB</code>\n"
        f"<b>RAM Percent (Swap):</b> <code>{psutil.swap_memory()[3]} %</code>\n\n"
        f"<b>• <u>Drive/Storage</u></b>\n"
        f"<b>Total Partitions:</b> <code>{len(psutil.disk_partitions())}</code>\n"
        f"<b>Disk Usage Total:</b> <code>{psutil.disk_usage('/')[0]/(1024**3):.2f} GB</code>\n"
        f"<b>Disk Usage Used:</b> <code>{psutil.disk_usage('/')[1]/(1024**3):.2f} GB</code>\n"
        f"<b>Disk Usage Free:</b> <code>{psutil.disk_usage('/')[2]/(1024**3):.2f} GB</code>\n"
        f"<b>Disk Usage Percent:</b> <code>{psutil.disk_usage('/')[3]} %</code>\n\n"
    )

    await Message.reply_msg(update, sys_info)
