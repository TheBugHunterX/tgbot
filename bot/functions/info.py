from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import MessageOriginType
from bot.helper.telegram_helper import Message, Button


async def func_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    re_msg = update.message.reply_to_message
    victim = user

    if re_msg:
        forward_origin = re_msg.forward_origin
        from_user = re_msg.from_user
    
        if forward_origin and forward_origin.type == MessageOriginType.USER:
            victim = forward_origin.sender_user
        
        if from_user and not forward_origin:
            victim = from_user
        
        if not victim:
            await Message.reply_message(update, f"<b>• Full name:</b> <code>{forward_origin.sender_user_name}</code>\n<i>Replied user account is hidden!</i>")
            return
    
    victim_photos = await victim.get_profile_photos()
    victim_pfp = None
    if victim_photos.photos:
        victim_pfp = victim_photos.photos[0][-1].file_id # returns victims latest pfp file id
    
    victim_username = f"@{victim.username}" if victim.username else None
    msg = (
        f"<b>• Full name:</b> <code>{victim.full_name}</code>\n"
        f"<b>  » First name:</b> <code>{victim.first_name}</code>\n"
        f"<b>  » Last name:</b> <code>{victim.last_name}</code>\n"
        f"<b>• Mention:</b> {victim.mention_html()}\n"
        f"<b>• Username:</b> {victim_username}\n"
        f"<b>• ID:</b> <code>{victim.id}</code>\n"
        f"<b>• Lang:</b> <code>{victim.language_code}</code>\n"
        f"<b>• Is bot:</b> <code>{victim.is_bot}</code>\n"
        f"<b>• Is premium:</b> <code>{victim.is_premium}</code>"
    )

    btn = await Button.ubutton([{"User Profile": f"tg://user?id={victim.id}"}]) if victim.username else None

    if victim_pfp:
        await Message.reply_image(update, victim_pfp, msg, btn=btn)
    else:
        await Message.reply_message(update, msg, btn=btn)
