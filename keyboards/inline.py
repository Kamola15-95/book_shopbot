from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_product_detail(product_id, quantity=1):
    markup = InlineKeyboardMarkup()
    minus_btn = InlineKeyboardButton(text='➖', callback_data='minus')
    quan_btn = InlineKeyboardButton(text=str(quantity), callback_data='quantity')
    plus_btn = InlineKeyboardButton(text='➕', callback_data='plus')
    cart_btn = InlineKeyboardButton(text='🛒 Корзина', callback_data='cart')
    buy_btn = InlineKeyboardButton(text='Хочу 😻', callback_data=f'buy_{product_id}')
    markup.add(minus_btn, quan_btn, plus_btn)
    markup.add(buy_btn)
    markup.add(cart_btn)
    return markup


def generate_cart_buttons(cart_products, cart_id):
    markup = InlineKeyboardMarkup()

    for cart_product in cart_products:
        name = InlineKeyboardButton(text=cart_product[2], callback_data='name')
        minus = InlineKeyboardButton(text='-1', callback_data=f'remove_{cart_product[0]}')
        quan_btn = InlineKeyboardButton(text=str(cart_product[3]), callback_data='quan')
        plus = InlineKeyboardButton(text='+1', callback_data=f'append_{cart_product[0]}')
        markup.row(name)
        markup.row(minus, quan_btn, plus)
    clear = InlineKeyboardButton(text='Очистить', callback_data=f'clear_{cart_id}')
    order = InlineKeyboardButton(text='Купить', callback_data=f'order_{cart_id}')
    main_menu = InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
    markup.row(clear, order)
    markup.row(main_menu)
    return markup

