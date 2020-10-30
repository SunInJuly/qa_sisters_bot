from random import randint

from aiogram import types
from telegram_bot_pagination import InlineKeyboardPaginator

from bot import db, dp, bot


@dp.message_handler(regexp='(^.*[#]?ваканси[я|и|ю].*?$)')
async def save_opening(message: types.Message):
    with open(f'saved_pics/{randint(1, 6)}.jpg', 'rb') as photo:
        db.add_message(message.text, message.from_user.username)
        await message.reply_photo(photo, caption='сохранил в копилочку')


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == "openings")
async def callback_openings(call):
    openings = db.get_items()

    async def send_opening(message, page=1):
        paginator = InlineKeyboardPaginator(
            len(openings),
            current_page=page,
            data_pattern='openings#{page}'
        )
        text = f"текст вакансии: {openings[page - 1].description}, \nПрислала: {openings[page - 1].contact}"

        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )

    page = int(call.data.split('#')[1])
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await send_opening(call.message, page)


@dp.message_handler(commands='openings-help')
async def show_openings_help(message):
    text = "Про вакансии: \n" \
           "- я сохраняю все #вакансии в базу \n" \
           "- чтобы посмотреть список всех вакансий набери команду /openings \n" \
           "- чтобы найти вакансию по ключевому слову набери /find (текст) \n" \
           "- чтобы удалить вакансию, набери /delete (текст) \n"

    await message.answer(text=text)


@dp.message_handler(commands='openings')
async def show_all_openings(call):
    openings = db.get_items()
    await show_openings(call, openings)


@dp.message_handler(commands='find')
async def find_opening(message: types.Message):
    openings = db.get_items()
    openings = list(filter(lambda opening: message.text.split('/find ')[1] in opening.description, openings))
    if len(openings) == 0:
        await message.reply("Упс, ничего не нашлось :(")
    else:
        await show_openings(message, openings)


@dp.message_handler(commands='delete')
async def delete_opening(message: types.Message):
    openings = db.get_items()
    if len(message.text.split('/delete ')) == 1:
        await message.reply("Укажите вакансию, которую мне надо удалить через пробел. Например /delete вакансия в мою "
                            "компанию")
        return

    openings = list(filter(lambda opening: message.text.split('/delete ')[1] in opening.description, openings))
    if len(openings) == 0:
        await message.reply("Упс, ничего не нашлось :(")
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        yes = types.InlineKeyboardButton(text="Да", callback_data=f"confirm#{openings[0].description}")
        keyboard.add(yes)
        await bot.send_message(message.chat.id,
                               f"Удаляем эту вакансию? \n {openings[0]}",
                               reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data.split("#")[0] == "confirm")
async def callback_delete_opening(call):
    db.delete_item(call.data.split("#")[1])
    await bot.send_message(chat_id=call.message.chat.id, text="Успешно удалена вакансия из базы")


async def show_openings(call, openings):
    paginator = InlineKeyboardPaginator(
        len(openings),
        data_pattern='openings#{page}'
    )

    text = f"Последняя присланная вакансия: \n" \
           f"текст вакансии: {openings[-1].description}" \
           f"\nПрислала: {openings[-1].contact}"

    await call.reply(
        text=text,
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
