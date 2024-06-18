import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from func_bot import fetch_vacancies

# The bot's token
bot = telebot.TeleBot('7294154285:AAFNdHIWUAzup8ZX37-_vBPKulDXF7o9PXM')

# Dictionary to keep track of user states (current page)
user_states = {}
ITEMS_PER_PAGE = 5


# Starting command
def start_command(message):
    bot.send_message(message.chat.id, 'Привет! 👋 Я бот, который поможет тебе найти интересные вакансии! Просто '
                                      'напиши \'/jobs\' и я помогу тебе найти работу!',
                                      reply_markup=types.ReplyKeyboardRemove())


# Function that shows buttons with job categories and sends data to on_click
def vacancies_command(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('IT-индустрия')
    btn2 = types.KeyboardButton('Образование')
    btn3 = types.KeyboardButton('Маркетинг')
    markup.row(btn1, btn2, btn3)

    btn4 = types.KeyboardButton('Менеджмент')
    btn5 = types.KeyboardButton('Финансы')
    btn6 = types.KeyboardButton('Продажи')
    markup.row(btn4, btn5, btn6)

    btn7 = types.KeyboardButton('Поддержка')
    btn8 = types.KeyboardButton('Без опыта')
    markup.row(btn7, btn8)

    bot.send_message(message.chat.id, 'Выбирай сферу из указанных ниже:', reply_markup=markup)

    bot.register_next_step_handler(message, on_click)


# Function that handles categories upon a button was pressed
def on_click(message):
    text = message.text.lower()
    chat_id = message.chat.id

    if text == 'it-индустрия':
        # Creating buttons under bot message
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Программист, Разработчик', callback_data='it_developer')
        btn2 = types.InlineKeyboardButton('Дата-сайентист, Аналитик', callback_data='it_analytics')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(chat_id, "Выберите сферу IT-индустрии:", reply_markup=markup)
    elif text == 'образование':
        bot.send_message(chat_id, 'Пожалуйста, подождите,\nэто может занять несколько секунд...',
                         reply_markup=types.ReplyKeyboardRemove())
        user_states[chat_id] = {'category': 'education', 'page': 0}
        data(message, page=0)
    elif text == 'маркетинг':
        bot.send_message(chat_id, 'Пожалуйста, подождите,\nэто может занять несколько секунд...',
                         reply_markup=types.ReplyKeyboardRemove())
        user_states[chat_id] = {'category': 'marketing', 'page': 0}
        data(message, page=0)
    elif text == 'менеджмент':
        bot.send_message(chat_id, 'Пожалуйста, подождите,\nэто может занять несколько секунд...',
                         reply_markup=types.ReplyKeyboardRemove())
        user_states[chat_id] = {'category': 'management', 'page': 0}
        data(message, page=0)
    elif text == 'финансы':
        bot.send_message(chat_id, 'Пожалуйста, подождите,\nэто может занять несколько секунд...',
                         reply_markup=types.ReplyKeyboardRemove())
        user_states[chat_id] = {'category': 'finances', 'page': 0}
        data(message, page=0)
    elif text == 'продажи':
        bot.send_message(chat_id, 'Пожалуйста, подождите,\nэто может занять несколько секунд...',
                         reply_markup=types.ReplyKeyboardRemove())
        user_states[chat_id] = {'category': 'sales', 'page': 0}
        data(message, page=0)
    elif text == 'поддержка':
        # Creating buttons under bot message
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Специалист Тех Поддержки', callback_data='techsupport_')
        btn2 = types.InlineKeyboardButton('Оператор Колл-Центра', callback_data='techsupport_callcenter')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(chat_id, "Выберите сферу:", reply_markup=markup)
    elif text == 'без опыта':
        bot.send_message(chat_id, 'Пожалуйста, подождите,\nэто может занять несколько секунд...',
                         reply_markup=types.ReplyKeyboardRemove())
        user_states[chat_id] = {'category': 'no_experience', 'page': 0}
        data(message, page=0)
    elif text == 'back':
        start_command(message)
    else:
        bot.send_message(chat_id, 'Я не понимаю эту команду. Возвращаю на старт.')
        start_command(message)


def data(message, page):
    chat_id = message.chat.id
    user_state = user_states[chat_id]

    # If such category was not found
    if not user_state:
        bot.send_message(chat_id, "Я не понимаю эту команду. Возвращаю на старт.")
        start_command(message)

    category = user_state['category']
    jobs = fetch_vacancies(category)

    if not jobs:
        bot.send_message(chat_id, "К сожалению, я не нашел вакансии по вашему запросу.")
        return

    # Get the jobs for the current page
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_jobs = jobs[start:end]

    # Format the fetched data
    list_str = "\n".join([
        (f"Позиция: {job['job_name']}\n"
         f"Компания: {job['company_name']}\n"
         f"Опыт: {job['experience']}\n"
         f"Зарплата: {job['salary']}\n"
         f"Ссылка на вакансию: {job['more_info']}\n"
         f"{'-' * 40}")
        for job in page_jobs
    ])

    # Create pagination buttons
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton('Back', callback_data='back')
    if page > 0:
        prev_button = types.InlineKeyboardButton('Previous page', callback_data=f'prev_{page - 1}')
        markup.row(prev_button)
    if end < len(jobs):
        next_button = types.InlineKeyboardButton('Next page', callback_data=f'next_{page + 1}')
        markup.row(next_button)
    markup.row(back_button)

    # Logic for not duplicating messages upon going through pages
    if 'message_id' in user_state:
        bot.edit_message_text(list_str, chat_id, user_state['message_id'], reply_markup=markup)
    else:
        sent_message = bot.send_message(chat_id, list_str, reply_markup=markup)
        user_state['message_id'] = sent_message.message_id


@bot.message_handler(commands=['start'])
def handle_start(message):
    start_command(message)


@bot.message_handler(commands=['jobs'])
def handle_vacancies(message):
    vacancies_command(message)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(('next_', 'prev_', 'back')))
def callback_message(callback):
    call_chat_id = callback.message.chat.id
    call_user_state = user_states[call_chat_id]

    if callback.data == 'back':
        vacancies_command(callback.message)
    else:
        action, call_page = callback.data.split('_')
        call_page = int(call_page)
        call_user_state['page'] = call_page
        data(callback.message, call_page)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('it_'))
def handle_it_subcategory(callback):
    chat_id = callback.message.chat.id
    subcategory = callback.data.split('_')[1].lower()

    bot.send_message(chat_id, 'Пожалуйста, подождите,\nэто может занять несколько секунд...',
                     reply_markup=types.ReplyKeyboardRemove())
    user_states[chat_id] = {'category': f'it_{subcategory}', 'page': 0}
    data(callback.message, page=0)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('techsupport_'))
def handle_techsupport_subcategory(callback):
    chat_id = callback.message.chat.id
    subcategory = callback.data.split('_')[1].lower()

    bot.send_message(chat_id, 'Пожалуйста, подождите,\nэто может занять несколько секунд...',
                     reply_markup=types.ReplyKeyboardRemove())
    user_states[chat_id] = {'category': f'techsupport_{subcategory}', 'page': 0}
    data(callback.message, page=0)


if __name__ == '__main__':
    bot.polling(none_stop=True)
