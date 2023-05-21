import telebot
from telebot import types
import psycopg2
import datetime
conn = psycopg2.connect(database="bot",
                        user="postgres",
                        password="123",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

token = '5411988825:AAGLPxyllrkMZDDBWIlTLuoOvTWkNqryySs'

bot = telebot.TeleBot(token)

today = datetime.datetime.today()
week_number = today.isocalendar()[1]

even_week = week_number % 2 == 0

if even_week:
    week_num = 2
else:
    week_num = 1

def get_timetable(day, week_num):
    query = f"SELECT subject, room_n, s_time, t_name FROM timetable WHERE day='{day}' AND week_n='{week_num}'"

    cursor.execute(query)
    rows = cursor.fetchall()

    timetable_str = f'Расписание на {day} (неделя {week_num}):\n\n'
    for row in rows:
        subject, room_n, s_time, t_name = row
        timetable_str += f'{s_time} - ({room_n})\n {subject}\n {t_name}\n\n'

    return timetable_str

def get_week(week_num):
    query = f"SELECT subject, room_n, s_time, t_name, day FROM timetable WHERE week_n='{week_num}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    week_str = f'Расписание на текущую неделю:\n\n'
    for row in rows:
        subject, room_n, s_time, t_name, day = row
        week_str += f'{day}\n{s_time} - ({room_n})\n {subject}\n {t_name}\n\n'
    return week_str

def get_n_week(week_num):
    query = f"SELECT subject, room_n, s_time, t_name, day FROM timetable WHERE week_n='{week_num}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    week_str = f'Расписание на следующую неделю:\n\n'
    for row in rows:
        subject, room_n, s_time, t_name, day = row
        week_str += f'{day}\n{s_time} - ({room_n})\n {subject}\n {t_name}\n\n'
    return week_str

@bot.message_handler(commands=['curr_week'])
def handle_timetable(message):
    if even_week:
        week_num = 2
    else:
        week_num = 1
    week_str = get_week(week_num)
    bot.send_message(message.chat.id, week_str)

@bot.message_handler(commands=['week'])
def handle_timetable(message):
    if even_week:
        week_str = 'Сегодня четная неделя'
    else:
        week_str = 'Сегодня нечетная неделя'
    bot.send_message(message.chat.id, week_str)

@bot.message_handler(commands=['next_week'])
def handle_timetable(message):
    if even_week:
        week_num = 1
    else:
        week_num = 2
    week_str = get_n_week(week_num)
    bot.send_message(message.chat.id, week_str)

@bot.message_handler(commands=['Monday'])
def monday(message):
    day = 'Понедельник'
    if even_week:
        week_num = 2
    else:
        week_num = 1
    timetable_str = get_timetable(day, week_num)
    bot.send_message(message.chat.id, timetable_str)

@bot.message_handler(commands=['Tuesday'])
def handle_timetable(message):
    day = 'Вторник'
    if even_week:
        week_num = 2
    else:
        week_num = 1
    timetable_str = get_timetable(day, week_num)
    bot.send_message(message.chat.id, timetable_str)

@bot.message_handler(commands=['Wednesday'])
def handle_timetable(message):
    day = 'Среда'
    if even_week:
        week_num = 2
    else:
        week_num = 1
    timetable_str = get_timetable(day, week_num)
    bot.send_message(message.chat.id, timetable_str)

@bot.message_handler(commands=['Thursday'])
def handle_timetable(message):
    day = 'Четверг'
    if even_week:
        week_num = 2
    else:
        week_num = 1
    timetable_str = get_timetable(day, week_num)
    bot.send_message(message.chat.id, timetable_str)

@bot.message_handler(commands=['Friday'])
def handle_timetable(message):
    day = 'Пятница'
    if even_week:
        week_num = 2
    else:
        week_num = 1
    timetable_str = get_timetable(day, week_num)
    bot.send_message(message.chat.id, timetable_str)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row('/help', '/mtuci',
                 '/curr_week', '/next_week',
                 '/week', '/Monday', '/Tuesday',
                 '/Wednesday', '/Thursday',
                 '/Friday')
    bot.send_message(message.chat.id, 'Привет! Я - бот с расписанием для группы БВТ2208. '
                                      'Напишите команду /help, чтобы узнать обо мне больше',
                     reply_markup=keyboard)

@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'Вся свежая информация о МТУСИ - https://mtuci.ru/')


@bot.message_handler(commands=['help'])
def start_message(message):
        bot.send_message(message.chat.id, 'Привет! Вот мои команды:\n/help - узнать о моих командах\n'
                                          '/curr_week - расписание на текущую неделю\n'
                                          '/next_week - расписание на следующую неделю\n'
                                          '/week - узнать какая сегодня неделя\n'
                                          '/Monday - расписание на понедельник текущей недели\n'
                                          '/Tuesday - расписание на вторник текущей недели\n'
                                          '/Wednesday - расписание на среду текущей недели\n'
                                          '/Thursday - расписание на четверг текущей недели\n'
                                          '/Friday - расписание на пятницу текущей недели\n'
                                          '/mtuci - узнать всю новую информацию о МТУСИ'
                         )


@bot.message_handler(content_types=['text'])
def answer_(message):
    if message.text.lower() not in ["/help", "/week", "/curr_week", "/next_week", "/Monday", "/Tuesday", "/Wednesday",
                                    "/Thursday", "/Friday", "/mtuci", '/start']:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')

bot.polling(none_stop=True)