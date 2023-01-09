import telebot, datetime
from telebot import types
from db_client import all_starters, all_hot_meals, all_desserts, all_drinks, insert_user_message, insert_user_click
from db_client import select_top_button, select_top_user
from secret import my_token

bot = telebot.TeleBot(my_token)

def menu():
    my_buttons = types.InlineKeyboardMarkup(row_width=2)
    button_starter = types.InlineKeyboardButton(text='Холодные закуски', callback_data='starter')
    button_hot_meal = types.InlineKeyboardButton(text='Горячие блюда', callback_data='hot_meal')
    button_dessert = types.InlineKeyboardButton(text='Десерты', callback_data='dessert')
    button_drink = types.InlineKeyboardButton(text='Напитки', callback_data='drink')
    my_buttons.add(button_starter, button_hot_meal, button_dessert, button_drink)
    return my_buttons

def to_home():
    home = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data='back')
    home.add(button)
    return home

def admin_menu():
    admin_buttons = types.InlineKeyboardMarkup(row_width=2)
    top_buttons = types.InlineKeyboardButton(text='Топ кнопок', callback_data='top_b')
    top_users = types.InlineKeyboardButton(text='Топ пользователей', callback_data='top_u')
    admin_buttons.add(top_buttons, top_users)
    return admin_buttons

def generate_message(type):
    msg = ''
    num = len(type)
    count = 0
    while count < num:
        msg += '<b>Блюдо: %s </b>\n%s \nРазмер порции: %s \n\nЦена: %s BYN \n\n' % (type[count][1], type[count][4], type[count][3], type[count][2])
        count += 1
    return msg

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.full_name}! Для того, чтобы ознакомиться с нашим меню, нажмите /menu.')

@bot.message_handler(commands=['menu'])
def mainmenu(message):
    bot.send_message(message.chat.id, 'Выберите тип блюда:', reply_markup=menu())

@bot.message_handler(commands=['admin'])
def admin(message):
    bot.send_message(message.chat.id, 'Выберите тип запроса:', reply_markup=admin_menu())

@bot.callback_query_handler(func=lambda call: True)
def info(call):

    if call.data == 'starter':
        name = call.from_user.full_name
        click_time = datetime.datetime.now()
        button = call.data
        insert_user_click(name, click_time, button)

        bot.send_message(chat_id=call.message.chat.id, text=generate_message(all_starters),
                         reply_markup=to_home(), parse_mode='html')

    if call.data == 'hot_meal':
        name = call.from_user.full_name
        click_time = datetime.datetime.now()
        button = call.data
        insert_user_click(name, click_time, button)

        bot.send_message(chat_id=call.message.chat.id, text=generate_message(all_hot_meals),
        reply_markup=to_home(), parse_mode='html')

    if call.data == 'dessert':
        name = call.from_user.full_name
        click_time = datetime.datetime.now()
        button = call.data
        insert_user_click(name, click_time, button)

        bot.send_message(chat_id=call.message.chat.id, text=generate_message(all_desserts),
        reply_markup=to_home(), parse_mode='html')

    if call.data == 'drink':
        name = call.from_user.full_name
        click_time = datetime.datetime.now()
        button = call.data
        insert_user_click(name, click_time, button)

        bot.send_message(chat_id=call.message.chat.id, text=generate_message(all_drinks),
        reply_markup=to_home(), parse_mode='html')

    if call.data == 'back':
        name = call.from_user.full_name
        click_time = datetime.datetime.now()
        button = call.data
        insert_user_click(name, click_time, button)

        bot.send_message(chat_id=call.message.chat.id, text="Вы вернулись в меню", reply_markup=menu())

    if call.data == 'top_b':
        n = '\n'
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"1 место: {select_top_button()[0][0]};{n}"
                              f"2 место: {select_top_button()[1][0]};{n}"
                              f"3 место: {select_top_button()[2][0]}.",
                         reply_markup=admin_menu(), parse_mode='html')

    if call.data == 'top_u':
        n = '\n'
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"1 место: {select_top_user()[0][0]};{n}"
                              f"2 место: {select_top_user()[1][0]};{n}"
                              f"3 место: {select_top_user()[2][0]}.",
                         reply_markup=admin_menu(), parse_mode='html')

@bot.message_handler(content_types='text')
def archieve(message):
    user_name = message.from_user.full_name
    text = message.text
    message_time = datetime.datetime.now()
    insert_user_message(user_name, text, message_time)

bot.polling(non_stop=True, interval=0)