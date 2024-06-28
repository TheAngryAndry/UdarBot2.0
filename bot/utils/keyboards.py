from aiogram import types
import json

def create_keyboard(call: str, data: list = None, formats_callback: dict = None,
                    formats_text: dict = None, formats_url: dict = None) -> types.ReplyKeyboardMarkup:
    """Create keyboard from json file or from data
    :param call: call of keyboard
    :param data: data for keyboard
    :param formats_callback: formats for callback of button
    :param formats_text: formats for text of buttons
    :param formats_url: formats for url of button
    :return: keyboard
    """
    # create empty keyboard
    keyboard = []

    # load json file with keyboard data
    if data is None:
        with open("bot/config/keyboards.json", "r", encoding="UTF-8") as file:
            data = json.load(file)
    #TODO: Create format text of buttons
    # itterate through json
    for keyboard_data in data:
        # if keyboard data is equal to call
        if keyboard_data["call"] == call:
            # itterate through keyboard rows 
            for i, row in enumerate(keyboard_data["keyboard"]):
                #add new row
                keyboard.append([])
                # itterate through buttons in row
                for button in row:
                    # if button is empty
                    if not button: continue
                    # format text and callback, url
                    if formats_text:
                        for key, value in formats_text.items():
                            try:
                                button["text"] = button["text"].replace(f'{{{key}}}', str(value))
                            except KeyError as e:
                                continue
                    if formats_callback:
                        for key, value in formats_callback.items():
                            try:
                                button["callback_data"] = button["callback_data"].replace(f'{{{key}}}', str(value))
                            except KeyError as e:
                                continue
                    if formats_url:
                        for key, value in formats_url.items():
                            try:
                                button["url"] = button["url"].replace(f'{{{key}}}', str(value))
                            except KeyError as e:
                                continue
                    # add button to row
                    keyboard[i].append(
                        types.InlineKeyboardButton(text=button["text"],
                                                    callback_data=button["callback_data"] if "callback_data" in button else None,
                                                    url=button["url"] if "url" in button else None,
                                                    web_app=button["web_app"] if "web_app" in button else None,
                                                    pay=button["pay"] if "pay" in button else False))
            break
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

def add_button(keyboard: types.InlineKeyboardMarkup, text: str,
               back_call: str = None, url: str = None,
               web_app: types.WebAppInfo = None,
               pay: bool = False) -> types.InlineKeyboardMarkup:
    """Add button to keyboard
    :param keyboard: keyboard
    :param back_call: callback data of button
    :param text: text of button
    :param pay: pay button
    :return: keyboard
    """
    # add button to keyboard
    return types.InlineKeyboardMarkup(inline_keyboard=[*keyboard.inline_keyboard,
                                                       [types.InlineKeyboardButton(text=text,
                                                                                   callback_data=back_call if back_call is not None else None,
                                                                                   url=url if url is not None else None,
                                                                                   web_app=web_app if web_app is not None else None,
                                                                                   pay=pay)]])
