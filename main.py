import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.types import ParseMode

API_TOKEN = '5483687091:AAEjLgw_bZFWUoDEf7QjiMiZK3ndfc8TX3g'

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    firstname = State()
    lastname = State()
    group = State()
    startedu = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await Form.firstname.set()
    await message.reply("qq, kak zovyt?")


@dp.message_handler(state=Form.firstname)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = message.text
    await Form.next()
    await message.reply('Napishi familiuy:')


@dp.message_handler(state=Form.lastname)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = message.text
    await Form.next()
    await message.reply("Napishi gruppu:")

@dp.message_handler(lambda message: message.text, state=Form.group)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await Form.next()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("2017", "2018", "2019", "2020")

    await message.reply("God postupleniya:", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["2017", "2018", "2019", "2020"], state=Form.startedu)
async def process_gender_invalid(message: types.Message):
    return await message.reply("Neverno bro")


@dp.message_handler(state=Form.startedu)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['startedu'] = message.text

        markup = types.ReplyKeyboardRemove()

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Rad vstreche, ', md.bold(data['firstname'] + " " + data['lastname'])),
                md.text('Gruppa: ', data['group']),
                md.text('Nachal putb samuraya v: ', data['startedu']),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,

        )

        await state.finish()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
