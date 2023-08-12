from aiogram.types import Message
from data.loader import bot, dp
from .text_handlers import start_register, show_main_menu, show_main_menu_admin
from data.loader import db
from keyboards.reply import generate_filials_information_commands, generate_main_menu_admin, generate_main_menu
ADMIN_ID = 477797263
ADMIN_IDS_FILE = "admin_ids.txt"

@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await message.answer('Добро пожаловать в интернет-магазин книг BookVerse!')
    # Начать регистрацию по номеру телефона
    user = db.get_user_by_id(message.chat.id)
    chat_id = message.chat.id
    if chat_id == ADMIN_ID:
        await message.answer('Выберите раздел:', reply_markup=generate_main_menu_admin())
    elif user:
        await message.answer('Выберите раздел:', reply_markup=generate_main_menu())
    else:
        await start_register(message)


@dp.message_handler(regexp='📖 О нас')
@dp.message_handler(commands=['about'])
async def command_feedback(message: Message):
    await message.answer('BookVerse - это онлайн-магазин, специализирующийся на продаже книг и обеспечивающий удобный и интерактивный опыт покупок для любителей чтения.')


@dp.message_handler(regexp='📍 Наши филиалы')
@dp.message_handler(commands=['filials'])
async def command_feedback(message: Message):
    await message.answer('Выберите филиал: ', reply_markup=generate_filials_information_commands())


@dp.message_handler(regexp='☎ Обратная связь')
@dp.message_handler(commands=['feedback'])
async def command_feedback(message: Message):
    await message.answer('📲 <b>Единый call-центр:</b> 1234 или (71) 123-45-67')

