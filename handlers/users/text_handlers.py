from aiogram.types import Message
from aiogram import types
from data.loader import bot, dp, db
from states.states import NumberState, YourStateEnum
from aiogram.dispatcher import FSMContext
import re
import aiohttp
from keyboards.reply import generate_main_menu, generate_main_menu_admin, generate_delivery_types, \
    generate_filials_list, generate_categories, generate_products, generate_admin_panel, generate_filials_information, \
    generate_information
from keyboards.inline import generate_product_detail, generate_cart_buttons


 # Регистрация пользовалей и назначение админа

ADMIN_ID = 477797263
ADMIN_IDS_FILE = "admin_ids.txt"

async def start_register(message: Message, state=None):
    await NumberState.phone.set()
    await message.answer('Отправьте свой номер телефона в формате: <b>+998 ** *** ** **</b>')

@dp.message_handler(state=NumberState.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text
    result1 = re.search(r'\+998 \d\d \d\d\d \d\d \d\d', phone)
    result2 = re.search(r'\+998\d{9}', phone)
    if result1 or result2:
        await message.answer('Ок')
        chat_id = message.chat.id
        full_name = message.from_user.full_name
        await state.finish()
        db.insert_user(chat_id, full_name, phone)
        await show_main_menu(message)
        if chat_id == ADMIN_ID:
        # Добавление ID администратора в файл или базу данных
            with open(ADMIN_IDS_FILE, "a") as file:
                file.write(str(chat_id) + "\n")
            await message.answer('Вы были назначены администратором.', reply_markup=generate_main_menu_admin())
    else:
        await message.answer('No')
        await state.finish()
        await again_start_register(message)

async def again_start_register(message: Message, state=None):
    await NumberState.phone.set()
    await message.answer('''Неверный номер телефона или запись. 
Напишите в этом формате: <b>+998 ** *** ** **</b>''')

  # -----------------------------Меню -------------------------------

@dp.message_handler(regexp='🏠 Главное меню')
async def show_main_menu(message: Message):
    chat_id = message.chat.id
    if chat_id == ADMIN_ID:
        await message.answer('Выберите раздел: ', reply_markup=generate_main_menu_admin())
    else:
        await message.answer('Выберите раздел: ', reply_markup=generate_main_menu())

@dp.message_handler(regexp='🧑 Админ-панель')
async def show_admin_panel(message: Message):
    chat_id = message.chat.id
    if chat_id == ADMIN_ID:
        await message.answer('Выберите раздел: ', reply_markup=generate_admin_panel())
    else:
        await message.answer('У вас нет доступа к админ-панели.')

@dp.message_handler(regexp='◀️ Назад в меню администратора')
async def show_main_menu_admin(message: Message):
    await message.answer('Выберите раздел: ', reply_markup=generate_main_menu_admin())

# @dp.message_handler(regexp='⚙ Настройки')

@dp.message_handler(regexp='◀ к категориям')
async def show_main_menu_admin(message: Message):
    await message.answer('Выберите категорию: ', reply_markup=generate_categories())


@dp.message_handler(regexp='📚 Каталог')
@dp.message_handler(regexp='🚗 к выбору доставки')
async def show_delivery_choice(message: Message):
    await message.answer('Выберите тип заказа: ', reply_markup=generate_delivery_types())

@dp.message_handler(lambda message: message.text == "🛒 Корзина")
async def show_cart_from_message(message: types.Message):
    chat_id = message.chat.id
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]

    db.update_cart_total_price_quantity(cart_id)
    total_price, total_quantity = db.get_cart_total_price_quantity(cart_id)
    try:
        total_price, total_quantity = int(total_price), int(total_quantity)
    except:
        total_price, total_quantity = 0, 0

    cart_products = db.cart_products_by_cart_id(cart_id)

    text = f'''Ваша корзина:\n\n'''

    for cart_product in cart_products:
        text += f'''{cart_product[2]} - {cart_product[3]} шт - {cart_product[4]} сум\n\n'''

    text += f'''Общее количество: {total_quantity} шт
Общая сумма: {total_price} сум'''

    await bot.send_message(chat_id, text, reply_markup=generate_cart_buttons(cart_products, cart_id))



@dp.message_handler(regexp='◀ к филиалам')
@dp.message_handler(regexp='🏃‍♀️Самовывоз')
async def show_filials_choice(message: Message):
    await message.answer('Выберите филиал: ', reply_markup=generate_filials_list())


filials = [i[0] for i in db.get_filials_names()]

@dp.message_handler(regexp='ℹ️ Информация')
@dp.message_handler(regexp='◀️ Назад')
async def show_information(message: Message):
    await message.answer('ℹ Информация', reply_markup=generate_information())

@dp.message_handler(regexp='🏘 Филиалы')
async def show_filials(message: Message):
    await message.answer('🏘 Выберите филиал: ', reply_markup=generate_filials_information())

@dp.message_handler(lambda message: message.text.startswith('🏘'))
async def show_filial_details(message: types.Message):
    selected_filials = message.text[1:].split(',')
    for selected_filial in selected_filials:
        filial_info = db.get_filial(selected_filial.strip())
        if filial_info:
            filial_name, worktime, address, preorder = filial_info
            coordinates = db.get_filial_coordinates(selected_filial.strip())
            if coordinates:
                latitude, longitude = coordinates
                latitude = float(latitude)
                longitude = float(longitude)
                location = types.Location(latitude=float(latitude), longitude=float(longitude))
                map_link = f'https://maps.google.com/?q={latitude},{longitude}'
                details_text = f'''
🏢 Филиал: {filial_name}
📍 Адрес: {address}
⌚️ Режим работы: {worktime}
📞 Предзаказ: {preorder}
🌍 Геолокация: {location.latitude}, {location.longitude}
🗺 Перейти в карты: {map_link}
                '''
            else:
                details_text = f'''
🏢 Филиал: {filial_name}
📍 Адрес: {address}
⌚️ Режим работы: {worktime}
🌍 Геолокация: Неизвестно
                '''
            await message.answer(details_text, reply_markup=generate_filials_information())
        else:
            await message.answer(f'Информация о филиале "{selected_filial}" недоступна.')


@dp.message_handler(lambda message: message.text in filials)
async def show_menu(message: Message):
    await message.answer('Выберите категорию: ', reply_markup=generate_categories())


categories = [i[0] for i in db.get_categories()]


@dp.message_handler(lambda message: message.text in categories)
async def show_products(message: Message):
    await message.answer('Выберите товар: ', reply_markup=generate_products(message.text))


products = [i[0] for i in db.get_all_products()]

@dp.message_handler(lambda message: message.text in products)
async def show_product_detail(message: Message):
    product = db.get_product_by_title(message.text)
    with open(product[6], mode='rb') as img:
        caption = f'Товар: {product[1]}\n\nЖанр: {product[2]}\n\nАвтор: {product[3]}\n\nОписание: {product[4]}\n\nЦена: {product[5]} сум'
        await bot.send_photo(chat_id=message.chat.id,
                             photo=img,
                             caption=caption,
                             reply_markup=generate_product_detail(product[0]))

#--------------------------------------------------------------------
# Обработчик для кнопки "Доставка"
@dp.message_handler(regexp= '🚗 Доставка')
async def handle_delivery(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    request_location_button = types.KeyboardButton(text="Отправить геопозицию", request_location=True)
    keyboard.add(request_location_button)

    await message.reply("Отправьте свою геопозицию:", reply_markup=keyboard)


# # Обработчик для получения геопозиции от пользователя
# @dp.message_handler(content_types=[types.ContentType.LOCATION])
# async def handle_location(message: types.Message):
#     latitude = message.location.latitude
#     longitude = message.location.longitude
#
#     address = await get_address_from_coordinates(latitude, longitude)
#
#     await message.reply(f"Ваше местоположение:\n{address}")

#-------------------------------------------------------------
async def get_address_from_coordinates(latitude, longitude):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(
                f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18") as response:
            data = await response.json()
            address = data.get('display_name', 'Адрес не найден')
            return address

# Обработчик для получения геопозиции от пользователя
@dp.message_handler(content_types=[types.ContentType.LOCATION])
async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    address = await get_address_from_coordinates(latitude, longitude)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.KeyboardButton(text="Подтвердить адрес")
    keyboard.add(confirm_button)

    # Сохраняем адрес в контексте пользователя
    await YourStateEnum.WaitingForAddressConfirmation.set()
    await message.reply(f"Ваше местоположение:\n{address}\n\nПожалуйста, подтвердите адрес кнопкой ниже:",
                        reply_markup=keyboard)


# Обработка подтверждения адреса и сохранения в базе
@dp.message_handler(lambda message: message.text.lower() == 'подтвердить адрес',
                    state=YourStateEnum.WaitingForAddressConfirmation)
async def confirm_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        latitude = data['latitude']
        longitude = data['longitude']
        address = data['address']

        db.insert_address(latitude, longitude, address)

        await message.reply("Адрес подтвержден и сохранен! Спасибо!", reply_markup=types.ReplyKeyboardRemove())

    # Сбрасываем состояние пользователя
    await state.finish()






