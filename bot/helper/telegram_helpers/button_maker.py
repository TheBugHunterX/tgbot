from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot import logger

class ButtonMaker:
    def ubutton(data: list):
        """
        **url button maker**\n
        :param data: `list` of `dict`\n
        *Note: same data in one `dict` will be in same row*
        """
        try:
            keyboard = []
            for keyboard_data in data:
                button = [InlineKeyboardButton(btn_name, btn_url) for btn_name, btn_url in keyboard_data.items()]
                keyboard.append(button)

            return InlineKeyboardMarkup(keyboard)
        except Exception as e:
            logger.error(e)


    def cbutton(data: list):
        """
        **callback button maker**\n
        :param data: `list` of `dict`\n
        *Note: same data in one `dict` will be in same row*
        """
        try:
            keyboard = []
            for keyboard_data in data:
                button = [InlineKeyboardButton(btn_name, callback_data=btn_data) for btn_name, btn_data in keyboard_data.items()]
                keyboard.append(button)
            
            return InlineKeyboardMarkup(keyboard)
        except Exception as e:
            logger.error(e)
