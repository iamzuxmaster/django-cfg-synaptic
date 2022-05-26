# Local Modules
from app import *
import buttons as btn
import strings
from genius import chunk, request, touched

# Aiogram Modules
from aiogram import types,Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext 
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Filter


storage = RedisStorage2('localhost', 6379, db=5, pool_size=10, prefix='my_fsm_key') if REDIS_STORAGE else MemoryStorage()


bot = Bot(BOT_TOKEN, parse_mode=types.message.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)



class States(StatesGroup):
    request_phone = State()
    request_language = State()


# state= States.request_phone or '*' <- all
@dp.message_handler(commands=['start'], state='*')
async def get_start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text=message.text)


@dp.message_handler(commands=['help'], state='*')
async def get_help(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    text = "This bot created with <b>pribot v1</b>"
    await bot.send_message(chat_id=chat_id, text=text)
    
    

@dp.callback_query_handler(text=["uz", "ru", "en"], state=States.request_language)
async def get_language(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id

    await state.finish()
    await States.request_phone.set()
    # or 
    # await States.next()

# Filter Number 
@dp.message_handler(content_types=["contact"], state=States.request_phone)
async def get_phone_number(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    #! Recomended 
    # phone_number = message.contact.phone_number.replace('+', '')

    await state.finish()


executor.start_polling(dp)