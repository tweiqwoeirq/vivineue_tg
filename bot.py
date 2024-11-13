import sqlite3
import time
from telebot import TeleBot, types

API_TOKEN = '7486472881:AAGjLZk8-FQCSakopM3hmAJ6_5UjLjkWG8A'
bot = TeleBot(API_TOKEN)

# функція для ініціалізації бази даних
def init_db():
    with sqlite3.connect('database.db') as db: # 1підключення
        cursor = db.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                phone TEXT,
                full_name TEXT,
                is_registered INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                category TEXT,
                name TEXT,
                photo TEXT,
                description TEXT,
                price REAL
            );
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                delivery_option TEXT,
                payment_method TEXT,
                order_status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
        ''')
        add_sample_products()  # зразкові товари
        db.commit()

def add_sample_products():
    with sqlite3.connect('database.db') as db: # 2підключення
        cursor = db.cursor()
        cursor.executescript('''
        delete from products; 
            INSERT INTO products (category, name, photo, description, price) VALUES
                ('ВЕРХ', 'Зіп-худі ERD Enfants Riches Déprimés', 'https://imgur.com/J0zRogq', 'Бавовняна зіп-худі з трикотажу з вінтажним ефектом у вигляді розривів і потертостей. У наявності розміри S, M, L.', 10100),
                ('ВЕРХ', 'Худі Maison Margiela', 'https://imgur.com/a/QuVsRXd', 'Чорний худі від Maison Margiela. Всі бірки присутні. Легіт-Орігінал. У наявності розміри S, M.', 7000),
                ('ВЕРХ', 'Футболка Vultures tee', 'https://imgur.com/a/pOhXNdg', 'Найкраща якість, є всі бирки, якісні матеріали та пошиття, щільний принт.  У наявності розмір L.', 3500),
                ('ВЕРХ', 'Худі Balenciaga Pink Polo', 'https://imgur.com/a/kdkazu9', 'Найкраща якість, є всі бирки, якісний принт, має такий самий крій, як і в оригіналі. У наявності розміри M, XL.', 4400),
                ('ВЕРХ', 'Худі Vetements LIMITED EDITION', 'https://imgur.com/a/P8BllEO', 'Чорний худі з білим написом "VETEMENTS LIMITED EDITION" на передній частині. Має передню кишеню та зав’язки на капюшоні. У наявності розміри S.', 7400),
                ('НИЗ', 'Джинси Ballon House', 'https://imgur.com/a/hbgguED', 'У наявності розмір L.', 5700),
                ('НИЗ', 'Джинси Baggy 7SKY', 'https://imgur.com/a/n9r95ZY', 'У наявності розміри S, M.', 5500),
                ('НИЗ', 'Джинси Acne Studio', 'https://imgur.com/a/cq5EAYq', 'У наявності розміри S, M, L.', 6000),
                ('НИЗ', 'Джинси No Brand', 'https://imgur.com/a/I73CfWB', 'У наявності розміри S, M.', 5400),
                ('НИЗ', 'Джинси Jaded London', 'https://imgur.com/a/jOqRWAj', 'У наявності розмір M.', 5500),
                ('ВЗУТТЯ', 'Кеди Vans Old Skool', 'https://imgur.com/a/VNPmzcw', 'У наявності 41-43 розмір.', 4500),
                ('ВЗУТТЯ', 'Кросівки Balenciaga V3C3', 'https://imgur.com/a/2IQZAmU', 'У наявності 37-38 розмір.', 17500),
                ('ВЗУТТЯ', 'Кросівки Balenciaga 10XL', 'https://imgur.com/a/PbAt4c3', 'У наявності 41-42 розмір.', 18900),
                ('ВЗУТТЯ', 'Кросівки Balenciaga 3XL', 'https://imgur.com/a/Kz9XeSq', 'У наявності 39 розмір.', 14500),
                ('ВЗУТТЯ', 'Кеди Rick Owens Hexa Sneaks', 'https://imgur.com/a/OqTrFJt', 'У наявності 41-44 розмір.', 12200),
                ('АКСЕСУАРИ', 'Рюкзак Anello', 'https://imgur.com/a/pWW9cet', 'Чорний рюкзак Anello з трьома різними патчами, які додають йому унікального вигляду. Рюкзак має основне відділення та передню кишеню на блискавці.', 2000),
                ('АКСЕСУАРИ', 'Кільце Сhrome hearts', 'https://imgur.com/a/CTCzIxt', 'Срібне кільце з унікальним хрестоподібним дизайном та круглим елементом посередині.', 4700),
                ('АКСЕСУАРИ', 'Сумка Mastermind Homme', 'https://imgur.com/a/ioOLhYN', 'Містка сумка, виготовлена ​​з щільних, надійних матеріалів. Є всі бирки.', 2200),
                ('АКСЕСУАРИ', 'Сумка Comme Des Garçons', 'https://imgur.com/a/jFRNAdF', 'Щільні матеріали, багато місця в сумці, можна носити через плече, є всі бирки.', 2900),
                ('АКСЕСУАРИ', 'Ремінь 1017 ALYX 9SM', 'https://imgur.com/cQXeSfS', '1017 Alyx 9SM — це американський бренд, заснований дизайнером Метью Вільямсом у 2015 році.  Дизайни 1017 Alyx 9SM поєднують у собі високу моду та скейт, панк-стиль. Довжина регулюється.', 3900);
        ''')
        db.commit()

# перга команда /start
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    with sqlite3.connect('database.db') as db: # 3підключення
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()

        if user and user[3]:  # перевірка реєстрації
            bot.reply_to(message, "_Ви вже зареєстровані. Перегляньте асортимент._", parse_mode='Markdown')
            show_main_menu(message)
        else:
            bot.reply_to(message, "_Будь ласка, введіть ваш номер телефону для реєстрації. Обов'язково у форматі +380._", parse_mode='Markdown')

# обробка тел
@bot.message_handler(func=lambda message: message.text.startswith("+"))
def handle_phone(message):
    user_id = message.from_user.id
    phone = message.text
    
    bot.reply_to(message, "_Будь ласка, введіть ваше ПІБ._", parse_mode='Markdown')
    bot.register_next_step_handler(message, handle_full_name, phone)

# обробка піб
def handle_full_name(message, phone):
    full_name = message.text
    user_id = message.from_user.id

    # збереження інфо в базі даних про користувача
    with sqlite3.connect('database.db') as db: # 4підключення
        cursor = db.cursor()
        cursor.execute("INSERT OR REPLACE INTO users (id, phone, full_name, is_registered) VALUES (?, ?, ?, ?)", 
                       (user_id, phone, full_name, 1))
        db.commit()

    bot.reply_to(message, "_Реєстрація успішна! Перегляньте асортимент._", parse_mode='Markdown')
    show_main_menu(message)

# основне меню
def show_main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Асортимент"), types.KeyboardButton("Розмірна сітка"), types.KeyboardButton("Розмірна сітка для взуття"), types.KeyboardButton("Умови доставки"))
    bot.send_message(message.chat.id, "_Оберіть опцію:_", reply_markup=keyboard, parse_mode='Markdown')

# вибір асортимент
@bot.message_handler(func=lambda message: message.text == "Асортимент")
def show_catalog_options(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("ВЕРХ"), types.KeyboardButton("НИЗ"), types.KeyboardButton("ВЗУТТЯ"), types.KeyboardButton("АКСЕСУАРИ"), types.KeyboardButton("Повернутись назад до меню"))
    bot.send_message(message.chat.id, "_Оберіть категорію асортименту:_", reply_markup=keyboard, parse_mode='Markdown')

# вибір розмірної сітки
@bot.message_handler(func=lambda message: message.text == "Розмірна сітка")
def show_size_chart(message):
    size_chart = (
        "*Розмірна сітка для загального одягу:*\n"
        "\n"
        "_XS: 32-34 (EU)_\n"
        "_S: 36-38 (EU)_\n"
        "_M: 40-42 (EU)_\n"
        "_L: 44-46 (EU)_\n"
        "_XL: 48-50 (EU)_\n"
        "_XXL: 52-54 (EU)_\n"
        "\n"
        "*Вимірювання можуть варіюватися залежно від моделі.*"
    )
    bot.reply_to(message, size_chart, parse_mode='Markdown')

# вибір розмірної сітки для взуття
@bot.message_handler(func=lambda message: message.text == "Розмірна сітка для взуття")
def show_shoe_size_chart(message):
    shoe_size_chart = (
        "*Розмірна сітка для взуття:*\n"
        "\n"
        "_36: 22.5 см_\n"
        "_37: 23.5 см_\n"
        "_38: 24.0 см_\n"
        "_39: 25.0 см_\n"
        "_40: 25.5 см_\n"
        "_41: 26.5 см_\n"
        "_42: 27.0 см_\n"
        "_43: 28.0 см_\n"
        "_44: 29.0 см_\n"
        "_45: 29.5 см_\n"
        "_46: 30.5 см_\n"
        "\n"
        "*Вимірювання можуть варіюватися залежно від моделі.*"
    )
    bot.reply_to(message, shoe_size_chart, parse_mode='Markdown')

# вибір умова доставки
@bot.message_handler(func=lambda message: message.text == "Умови доставки")
def show_delivery_terms(message):
    delivery_terms = (
        "*Умови доставки:*\n"
        "\n"
        "*1. Укрпошта:* стандартна доставка (_3-7 днів_).\n"
        "*2. Нова Пошта:* швидка доставка (_1-2 дні_).\n"
        "*3. Міст Пошта:* доставка до відділення (_2-5 днів_).\n"
        "\n"
        "_Вартість доставки залежить від компанії та місця призначення._"
    )
    bot.reply_to(message, delivery_terms, parse_mode='Markdown')

# вибір категорії
@bot.message_handler(func=lambda message: message.text in ["ВЕРХ", "НИЗ", "ВЗУТТЯ", "АКСЕСУАРИ"])
def show_products(message):
    category = message.text
    with sqlite3.connect('database.db') as db: #останнє підключення
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products WHERE category=?", (category,))
        products = cursor.fetchall()
        
        if products:
            for product in products:
                # інлайн кнопка замовлення під товаром
                keyboard = types.InlineKeyboardMarkup()
                order_button = types.InlineKeyboardButton("🛒 ЗАМОВИТИ", callback_data=f"order_{product[0]}")  # product[0] - айді товару
                keyboard.add(order_button)
                
                # відправка фото з описом товару
                bot.send_photo(message.chat.id, product[3], caption=f"{product[2]}\n{product[4]}\n💵 Ціна: {product[5]}", reply_markup=keyboard)
                time.sleep(0.5)
        else:
            bot.reply_to(message, "")

     # додаток після показу всіх товарів (візуально кнопка інлайн є, але функціонально вона не реагує) 
    bot.send_message(message.chat.id, "Вибачте за тимчасові незручності. На даний момент через нашого бота неможливо замовити товар, який вас цікавить, але ви можете зробити це, заповнивши анкету отримувача за посиланням: https://forms.gle/3BZHwV747oSrb85m6.")

    # кнопка повернення назад до меню
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🔙 Повернутись назад до меню"))
    bot.send_message(message.chat.id, "_Натисніть кнопку нижче, щоб повернутись._", reply_markup=keyboard, parse_mode='Markdown')

# опрацювання кнопки повернення назад до меню
@bot.message_handler(func=lambda message: message.text == "🔙 Повернутись назад до меню")
def back_to_main_menu(message):
    show_main_menu(message)

# опрацювання замовлення
@bot.callback_query_handler(func=lambda call: call.data.startswith("order_"))
def handle_order(call):
    product_id = call.data.split("_")[1]  # отримання айді товару
    user_id = call.from_user.id

    bot.answer_callback_query(call.id, "Товар додано!")
    bot.send_message(call.from_user.id, f"Ви замовили товар з ID: {product_id}. Очікуйте на зворотній зв'язок від менеджера Vivienue_shop. Дякуємо.")

# запуск
if __name__ == '__main__':
    init_db()
    bot.polling()
