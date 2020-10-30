import config
from aiogram import Bot, Dispatcher, executor
from dbhelper import DBHelper


bot = Bot(token=config.token)
dp = Dispatcher(bot)
db = DBHelper()

from handlers.openings import *

@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    welcome_text = "Привет! Я бот-помощник из чата QA sisters" \
                   "Что я умею: \n" \
                   "- я сохраняю посты с хештегом #вакансии (и напоминаю его ставить) \n" \
                   "- отдавать сохраненные вакансии по команде /openings \n" \
                   "- подробнее о командах с вакансиями: /openings-help \n" \
                   "- мне можно задать анонимный вопрос, и я перешлю его текст в чат (в работе) \n" \
                   "- я приветствую новичков в чате и напоминаю рассказать о себе (в работе) \n"

    await message.answer(text=welcome_text)


@dp.message_handler(lambda message: any(entity.type in ["url", "text_link"] for entity in message.entities))
async def save_link(message: types.Message):
    await message.reply("выглядит как интересная ссылка! Может, добавить её в полезности?")

if __name__ == '__main__':
    db.setup()
    executor.start_polling(dp)

