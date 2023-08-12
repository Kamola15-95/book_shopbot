from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import db

def generate_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    catalog = KeyboardButton(text='📚 Каталог')
    my_orders = KeyboardButton(text='📖 Мои заказы')
    filials = KeyboardButton(text='📍 Наши филиалы')
    feedback = KeyboardButton(text='☎️ Обратная связь')
    info = KeyboardButton(text='ℹ️ Информация')
    settings = KeyboardButton(text='⚙ Настройки')
    markup.row(catalog)
    markup.row(my_orders, filials)
    markup.row(feedback, info)
    markup.row(settings)
    return markup

def generate_main_menu_admin():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    catalog = KeyboardButton(text='📚 Каталог')
    my_orders = KeyboardButton(text='📝 Мои заказы')
    filials = KeyboardButton(text='📍 Наши филиалы')
    feedback = KeyboardButton(text='☎️ Обратная связь')
    info = KeyboardButton(text='ℹ️ Информация')
    settings = KeyboardButton(text='⚙ Настройки')
    admin_panel = KeyboardButton(text='🧑 Админ-панель')
    markup.row(catalog)
    markup.row(my_orders, filials)
    markup.row(feedback, info)
    markup.row(settings, admin_panel)
    return markup

def generate_admin_panel():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    add_item = KeyboardButton(text='⬇️ Добавить товар')
    delete_item = KeyboardButton(text='❌ Удалить товар')
    forward = KeyboardButton(text='📮 Сделать рассылку')
    back_btn = KeyboardButton(text='◀️ Назад в меню администратора')
    markup.row(add_item)
    markup.row(delete_item)
    markup.row(forward)
    markup.row(back_btn)
    return markup

def generate_delivery_types():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    delivery = KeyboardButton(text='🚗 Доставка')
    self_delivery = KeyboardButton(text='🏃‍♀️Самовывоз')
    back_btn = KeyboardButton(text='🏠 Главное меню')
    markup.row(delivery, self_delivery)
    markup.row(back_btn)
    return markup


def generate_filials_list():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_btn = KeyboardButton(text='🚗 к выбору доставки')
    filials = db.get_filials_names()
    buttons = []
    for filial in filials:
        btn = KeyboardButton(text=filial[0])
        buttons.append(btn)
    markup.add(back_btn)
    markup.add(*buttons)
    return markup

def generate_information():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    filials = KeyboardButton(text='🏘 Филиалы')
    moby_app = KeyboardButton(text='️📱Мобильное приложение')
    public = KeyboardButton(text='📑 Публичная оферта')
    main_btn = KeyboardButton(text='🏠 Главное меню')
    markup.row(filials)
    markup.row(moby_app)
    markup.row(public)
    markup.row(main_btn)
    return markup

def generate_filials_information():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_btn = KeyboardButton(text='◀️ Назад')
    filials = db.get_filials_names()  # Получение списка названий филиалов
    buttons = []
    for filial in filials:
        btn = KeyboardButton(text=f'🏘{filial[0]}')
        buttons.append(btn)
    markup.add(back_btn)
    markup.add(*buttons)
    return markup

def generate_filials_information_commands():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main_btn = KeyboardButton(text='🏠 Главное меню')
    filials = db.get_filials_names()  # Получение списка названий филиалов
    buttons = []
    for filial in filials:
        btn = KeyboardButton(text=f'🏘{filial[0]}')
        buttons.append(btn)
    markup.add(main_btn)
    markup.add(*buttons)
    return markup

def generate_categories():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    cart = KeyboardButton(text='🛒 Корзина')
    back_btn = KeyboardButton(text='◀ к филиалам')
    main_btn = KeyboardButton(text='🏠 Главное меню')
    categories = [i[0] for i in db.get_categories()]
    buttons = []
    for category in categories:
        btn = KeyboardButton(text=category)
        buttons.append(btn)
    markup.add(back_btn, cart, *buttons, main_btn)
    return markup


def generate_products(category_title):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    cart = KeyboardButton(text='🛒 Корзина')
    back_btn = KeyboardButton(text='◀ к категориям')
    main_btn = KeyboardButton(text='🏠 Главное меню')
    products = [i[0] for i in db.get_product_by_category(category_title)]
    buttons = []
    for product in products:
        btn = KeyboardButton(text=product)
        buttons.append(btn)
    markup.add(back_btn, cart, *buttons, main_btn)
    return markup
