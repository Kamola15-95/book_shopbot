from data.loader import bot, dp, db
from aiogram import types
from aiogram.types import CallbackQuery, LabeledPrice, ShippingOption
from keyboards.inline import generate_product_detail, generate_cart_buttons
from keyboards.reply import generate_main_menu, generate_main_menu_admin
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@dp.callback_query_handler(lambda call: call.data == 'plus')
async def reaction_to_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    buttons = call.message.reply_markup.inline_keyboard
    quantity = int(buttons[0][1].text)
    print(quantity)
    product_id = int(buttons[1][0].callback_data.split('_')[1]) # 0 - buy
    print(product_id)
    if quantity < 5:
        quantity += 1
        await bot.edit_message_reply_markup(chat_id, call.message.message_id,
            reply_markup=generate_product_detail(product_id, quantity))
    else:
        await bot.answer_callback_query(call.id, 'Нельзя купить более 5 товаров')


@dp.callback_query_handler(lambda call: call.data == 'minus')
async def reaction_to_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    buttons = call.message.reply_markup.inline_keyboard
    quantity = int(buttons[0][1].text)
    print(quantity)
    product_id = int(buttons[1][0].callback_data.split('_')[1]) # 0 - buy
    print(product_id)
    if quantity > 1:
        quantity -= 1
        await bot.edit_message_reply_markup(chat_id, call.message.message_id,
            reply_markup=generate_product_detail(product_id, quantity))
    else:
        await bot.answer_callback_query(call.id, 'Нельзя купить менее 1 товара')


@dp.callback_query_handler(lambda call: 'buy' in call.data)
async def add_product_to_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0] # (1, ) -> 1
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]
    _, product_id = call.data.split('_') # buy_1 -> 1
    product = db.get_product_by_id(product_id)
    product_title, price = product[1], product[5]
    quantity = int(call.message.reply_markup.inline_keyboard[0][1].text)
    final_price = price * quantity
    print(final_price)

    try:
        '''Попытка закинуть товар в корзину'''
        db.insert_cart_product(cart_id, product_title, quantity, final_price)
        await bot.answer_callback_query(call.id, 'Товар успешно добавлен')
    except:
        '''Если такой товар есть, то прибавить цену и количество'''
        db.update_cart_product(cart_id, product_title, quantity, final_price)
        await bot.answer_callback_query(call.id, 'Кол-во успешно изменено')


@dp.callback_query_handler(lambda call: 'cart' == call.data)
async def show_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
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

    print(total_price, total_quantity, cart_products)

    text = f'''Ваша корзина:\n\n'''

    for cart_product in cart_products:
        text += f'''{cart_product[2]} - {cart_product[3]} шт - {cart_product[4]} сум\n\n'''

    text += f'''Общее количество: {total_quantity} шт
Общая сумма: {total_price} сум'''

    await bot.send_message(chat_id, text, reply_markup=generate_cart_buttons(cart_products, cart_id))


# Обработчик для кнопки "Главное меню"
@dp.callback_query_handler(lambda call: call.data == 'main_menu')
async def show_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    if chat_id == 477797263:
        await bot.send_message(chat_id, 'Выберите раздел:', reply_markup=generate_main_menu_admin())
    else:
        await bot.send_message(chat_id, 'Выберите раздел:', reply_markup=generate_main_menu())


# Обработчик для кнопки "Очистить"

@dp.callback_query_handler(lambda call: call.data.startswith('clear_'))
async def clear_callback(call: CallbackQuery):
    cart_id = int(call.data.split('_')[1])  # Идентификатор корзины из callback_data

    # Очищаем корзину в базе данных
    db.clear_cart(cart_id)

    chat_id = call.message.chat.id
    await bot.answer_callback_query(call.id, text='Корзина очищена')
    await update_cart_message(chat_id, call.message.message_id)  # Обновляем сообщение с корзиной


# ---------------------------------------------------------------------------

async def update_cart_message(chat_id, message_id):
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

    markup = generate_cart_buttons(cart_products, cart_id)
    await bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=markup)

# @dp.callback_query_handler(lambda call: call.data.startswith('remove_'))
# async def minus_callback(call: CallbackQuery):
#     chat_id = call.message.chat.id
#     buttons = call.message.reply_markup.inline_keyboard
#     quantity = int(buttons[1][1].text)
#     product_id = int(buttons[1][0].callback_data.split('_')[1])  # 0 - buy
#     if quantity > 1:
#         quantity -= 1
#
#         # Здесь вы должны обновить количество на кнопке внутри разметки
#         buttons[1][1].text = str(quantity)  # Обновляем текст кнопки с количеством товара
#
#         # Обновляем разметку кнопок в сообщении
#         await bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
#
#         await update_cart_message(chat_id, call.message.message_id)  # Обновляем сообщение с корзиной
#     else:
#         await bot.answer_callback_query(call.id, 'Нельзя купить менее 1 товара')
#
#
# @dp.callback_query_handler(lambda call: call.data.startswith('append_'))
# async def plus_callback(call: CallbackQuery):
#     chat_id = call.message.chat.id
#     buttons = call.message.reply_markup.inline_keyboard
#     quantity = int(buttons[1][1].text)
#     print(quantity)
#     product_id = int(buttons[1][0].callback_data.split('_')[1])  # 0 - buy
#     print(product_id)
#     if quantity < 5:
#         quantity += 1
#         await bot.edit_message_reply_markup(chat_id, call.message.message_id,
#                                             reply_markup=generate_product_detail(product_id, quantity))
#         await update_cart_message(chat_id, call.message.message_id)  # Обновляем сообщение с корзиной
#     else:
#         await bot.answer_callback_query(call.id, 'Нельзя купить более 5 товаров')

# ---------------------------------------------------------------------------

@dp.callback_query_handler(lambda call: 'order' in call.data)
async def payment(call: CallbackQuery):
    chat_id = call.message.chat.id
    cart_id = call.data.split('_')[1]
    products = db.cart_products_by_cart_id(cart_id)
    print(products)
    await bot.send_invoice(chat_id=chat_id,
                           title=f'Чек для {call.message.from_user.full_name}',
                           description=''.join([f'{product[2]}\n' for product in products]),
                           payload='shop_bot',
                           start_parameter='create_invoice_products',
                           currency='UZS',
                           prices=[
                               LabeledPrice(
                                   label=f'{product[2]} - {product[3]} шт',
                                   amount=int(product[4] * 100)
                               ) for product in products
                           ],
                           need_name=True,
                           is_flexible=True,
                           need_shipping_address=True,
                           provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'
                           )


EXPRESS_SHIPPING = ShippingOption(
    id='post_express',
    title='Доставка за 1 час'
).add(LabeledPrice('Доставка за 1 час', 15_000_00))

REGULAR_SHIPPING = ShippingOption(
    id='post_regular',
    title='Самовывоз'
).add(LabeledPrice('Самовывоз', 0))


@dp.shipping_query_handler(lambda query: True)
async def shipping(shipping_query):
    await bot.answer_shipping_query(shipping_query.id,
                              ok=True,
                              shipping_options=[REGULAR_SHIPPING, EXPRESS_SHIPPING],
                              error_message='Простите, что-то не так')


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre):
    await bot.answer_pre_checkout_query(pre.id,
                                        ok=True,
                                        error_message='Опять что-то не так')



@dp.message_handler(content_types=['successful_payment'])
async def success(message):
    # Отправить админу всю инфу о заказе
    # Очистить пользователю корзину
    await bot.send_message(message.chat.id, 'Ура! Оплата прошла успешно! Мы вас кинули!!!!')

