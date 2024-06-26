import json
import os
import random

from bot.utils.models import Word, UserWord


async def create_text(call: str, formats=None) -> str:
    # load json file with texts
    with open('bot/config/texts.json', 'r', encoding="UTF-8") as file:
        data = json.load(file)

    # format 
    if formats:
        for key, value in formats.items():
            data[call] = data[call].replace(f'{{{key}}}', str(value))
    return data[call]


async def rnd_w_list(k: int,
                     exclude: list[Word] | None = None) -> list[Word]:  # generate random list of words for person to answer
    if exclude is None:
        data = await Word.find_many().to_list()
    else:
        exclude_ids = [i.id for i in exclude]
        data = await Word.find_many(Word.id not in exclude_ids).to_list()
    return random.sample(data, k=k)


async def load_words():
    data = await Word.find_many().to_list()
    if data:
        return
    with open(os.getcwd() + '/bot/public/words.txt') as f:
        await Word.insert_many([
            Word(send_word=i.rstrip().lower(), right_word=i.rstrip().replace('ё', 'е').replace('Ё', 'Е')) for i in
            f.readlines()
        ])
