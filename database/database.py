import sqlite3

class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('shop.db', check_same_thread=False)

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result


    def create_users_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(100),
            phone VARCHAR(20) UNIQUE
        )'''
        self.manager(sql, commit=True)


    def get_user_by_id(self, telegram_id):
        sql = '''
        SELECT * FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)


    def insert_user(self, telegram_id, full_name, phone):
        sql = '''
        INSERT INTO users(telegram_id, full_name, phone) VALUES (?,?,?)
        '''
        self.manager(sql, telegram_id, full_name, phone, commit=True)

    def create_filials_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS filials(
            filial_id INTEGER PRIMARY KEY AUTOINCREMENT,
            filial_name VARCHAR(100),
            places INTEGER,
            worktime VARCHAR(100),
            address VARCHAR(100),
            preorder TEXT
        )
        '''
        self.manager(sql, commit=True)


    def insert_filials(self):
        sql = '''
        INSERT INTO filials(filial_name, worktime, address, preorder) VALUES
        ('ЦУМ - Книжные ряды', '9:00-20:00', 'Улица Узбекистанская, 17, ориентир: метро Космонавтов', 'Предзаказ книг по номеру: +998 (90) 123-45-67'),
        ('Мирабад', '9:00-20:00', 'Улица Садыка Азимова, 43, ориентир:  бизнес-центр Glaeser-st', 'Предзаказ книг по номеру: +998 (90) 123-45-67'),
        ('Лабзак', '9:00-20:00', 'Улица А.Кадыри, 33, ориентир: парк Анхор', 'Предзаказ книг по номеру: +998 (90) 123-45-67'),
        ('Хадра', '9:00-20:00', 'Улица Себзар, 22, ориентир: метро Гафура Гуляма', 'Предзаказ книг по номеру: +998 (90) 123-45-67')
        '''
        self.manager(sql, commit=True)


    def get_filials_names(self):
        sql = '''
        SELECT filial_name FROM filials;
        '''
        return self.manager(sql, fetchall=True)


    def get_filial(self, filial_name):
        sql = '''
        SELECT filial_name, worktime, address, preorder FROM filials WHERE filial_name = ?
        '''
        return self.manager(sql, filial_name, fetchone=True)

    def create_coordinates_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS coordinates(
            coordinate_id INTEGER PRIMARY KEY AUTOINCREMENT,
            filial_id INTEGER,
            latitude REAL,
            longitude REAL,
            FOREIGN KEY (filial_id) REFERENCES filials (filial_id)
        )
        '''
        self.manager(sql, commit=True)

    def insert_coordinates(self):
        sql = '''
        INSERT INTO coordinates(filial_id, latitude, longitude) VALUES
        (1, 41.3076, 69.269739),
        (2, 41.31032, 69.291771),
        (3, 41.3218602, 69.2507297),
        (4, 41.323358, 69.244487)
        '''
        self.manager(sql, commit=True)

    def get_filial_coordinates(self, filial_name):
        sql = '''
        SELECT latitude, longitude FROM coordinates
        INNER JOIN filials ON filials.filial_id = coordinates.filial_id
        WHERE filials.filial_name = ?
        '''
        return self.manager(sql, filial_name, fetchone=True)

    def create_categories_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_title VARCHAR(50) UNIQUE
        )
        '''
        self.manager(sql, commit=True)

    def insert_categories(self):
        sql = '''
        INSERT INTO categories(category_title) VALUES 
        ('📊 Деловая и бизнес литература'),
        ('🔍 Детективы и триллеры'),
        ('🎳 Дом, хобби'),
        ('🧸 Детская литература'),
        ('🎭 Романы'),
        ('🔬 Наука'),
        ('🧗‍♀️Приключения'),
        ('🧘 Психология'),
        ('🎑 Фантастика')
        '''
        self.manager(sql, commit=True)

    def get_categories(self):
        sql = '''
        SELECT category_title FROM categories
        '''
        return self.manager(sql, fetchall=True)

    def create_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_title VARCHAR(100),
            genre VARCHAR(100),
            author VARCHAR(100),
            description VARCHAR(255),
            price INTEGER,
            image TEXT,
            category_id INTEGER REFERENCES categories(category_id) 
        )
        '''
        self.manager(sql, commit=True)


    def insert_products(self):
        sql = '''
        INSERT INTO products(product_title, genre, author, description, price, image, category_id)
        VALUES
        ('Думай медленно, решай быстро','📊 Деловая и бизнес литература','Дэниел Канеман','Канеман — психолог и лауреат Нобелевской премии по экономике. В книге он исследует, как интуиция и мышление работают вместе и помогают нам принимать решения.', 120000, 'images/2.jpeg', 1),
        ('В работу с головой. Паттерны успеха от IT-специалиста','📊 Деловая и бизнес литература','Кэл Ньюпорт','Автор делится подходом к работе, который позволяет быстро усваивать сложную информацию и добиваться лучших результатов за меньшее время.', 125000, 'images/3.jpeg', 1),
        ('Nudge. Архитектура выбора','📊 Деловая и бизнес литература','Ричард Талер и Касс Санстейн','Это книга о поведенческой экономике и способах «подталкивать» людей к определённым решениям и действиям, не лишая их свободы выбора.', 120000, 'images/4.png', 1),
        ('Илон Маск. Tesla, SpaceX и дорога в будущее','📊 Деловая и бизнес литература','Эшли Вэнс','Книга начинается с детства Маска и заканчивается основанием его главных компаний. При этом Вэнс не просто пишет, что происходило в жизни бизнесмена в разное время.', 120000, 'images/5.png', 1),
        ('Лунный камень', 'Детективы и триллеры', 'Уилки Коллинз', 'Знаменитый английский писатель заставляет разгадывать не только своих героев, но и читателей, которым он дает в руки лишь ниточку от клубка запутанных событий.', 90000, 'images/1.jpeg', 2)
        '''
        self.manager(sql, commit=True)


    def drop_products(self):
        sql = '''DROP TABLE IF EXISTS products'''
        self.manager(sql, commit=True)


    def get_product_by_category(self, category_title):
        sql = '''
        SELECT product_title FROM products WHERE category_id = (
            SELECT category_id FROM categories WHERE category_title = ?
        )
        '''
        return self.manager(sql, category_title, fetchall=True)


    def get_all_products(self):
        sql = '''
        SELECT product_title FROM products;
        '''
        return self.manager(sql, fetchall=True)

    def get_product_by_title(self, product_title):
        sql = '''
        SELECT * FROM products WHERE product_title = ?
        '''
        return self.manager(sql, product_title, fetchone=True)


    def create_cart_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cart(
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER REFERENCES users(telegram_id),
            total_quantity INTEGER DEFAULT 0,
            total_price INTEGER DEFAULT 0
        )
        '''
        self.manager(sql, commit=True)


    def create_cart_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cart_products(
            cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER REFERENCES cart(cart_id),
            product_title VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL,
            final_price INTEGER NOT NULL,
            
            UNIQUE(cart_id, product_title)
        )
        '''
        self.manager(sql, commit=True)


    def create_cart_for_user(self, telegram_id):
        sql = '''
        INSERT INTO cart(telegram_id) VALUES (?)
        '''
        self.manager(sql, telegram_id, commit=True)


    def get_cart_id(self, telegram_id):
        sql = '''
        SELECT cart_id FROM cart WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)


    def get_product_by_id(self, product_id):
        sql = '''
        SELECT * FROM products WHERE product_id = ?
        '''
        return self.manager(sql, product_id, fetchone=True)


    def insert_cart_product(self, cart_id, product_title, quantity, final_price):
        sql = '''
            INSERT INTO cart_products(cart_id, product_title, quantity, final_price)
            VALUES (?,?,?,?)
        '''
        self.manager(sql, cart_id, product_title, quantity, final_price, commit=True)


    def update_cart_product(self, cart_id, product_title, quantity, final_price):
        sql = '''
        UPDATE cart_products
        SET
        final_price = final_price + ?,
        quantity = quantity + ?
        WHERE product_title = ? AND cart_id = ?
        '''
        self.manager(sql, final_price, quantity, product_title, cart_id, commit=True)



    def update_cart_total_price_quantity(self, cart_id):
        sql = '''
        UPDATE cart 
        SET 
        total_quantity = (
            SELECT SUM(quantity) FROM cart_products WHERE cart_id = ?
        ),
        total_price = (
            SELECT SUM(final_price) FROM cart_products WHERE cart_id = ?
        )
        WHERE cart_id = ?
        '''
        self.manager(sql, cart_id, cart_id, cart_id, commit=True)


    def get_cart_total_price_quantity(self, cart_id):
        sql = '''
        SELECT total_price, total_quantity FROM cart WHERE cart_id = ?
        '''
        return self.manager(sql, cart_id, fetchone=True)


    def cart_products_by_cart_id(self, cart_id):
        sql = '''
        SELECT * FROM cart_products WHERE cart_id = ?
        '''
        return self.manager(sql, cart_id, fetchall=True)

    def clear_cart(self, cart_id):
        sql = '''
        DELETE FROM cart_products WHERE cart_id = ?
        '''
        return self.manager(sql, cart_id, fetchall=True)

    def create_address_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT
        )
        '''
        return self.manager(sql, commit=True)

    def insert_address(self, address):
        sql = '''
        INSERT INTO addresses (address) VALUES (?)
        '''
        return self.manager(sql, address, commit=True)

