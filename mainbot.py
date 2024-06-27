import telebot
import re
from telebot import types

bot = telebot.TeleBot('7360334831:AAFHK7hUgud6gtYBh6HfeG7YU-xMpPLRolA')

balance = 0
budget = 0
goal = 0
goaltext = "/dQDVSCVdssrg"
history = [None] * 1000
historytext = [None] * 1000
NowPos = 0



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в финансового телеграмм бота\nЯ могу: \nДобавление доходов и расходов: - Команда /addincome [сумма] [описание] для добавления дохода.\n .- Команда /addexpense [сумма] [описание] для добавления расхода.\n\n2. Просмотр баланса:- Команда /balance для вывода текущего баланса\n\n3. Установка и отслеживание бюджета:- Команда /setbudget [сумма] для установки месячного бюджета.\n- Команда /budget для проверки текущего состояния бюджета.\n\n4. Получение отчетов: - Команда /report [период] для получения отчета о доходах и расходах за указанный период.\n\n5. Категоризация расходов: Напоминания о финансовых целях:\n- Команда /setgoal [цель] [сумма] для установки финансовойцели.- Команда /goals для просмотра прогресса по финансовым целям.")

@bot.message_handler(commands = 'addincome')
def addincome( message):
    s = message.text
    symbols_to_remove = "/addincome  "

    for symbol in symbols_to_remove:
        s = s.replace(symbol, "")

    numbers = [int(x) for x in re.findall(r'\d+', s)]
    text_without_numbers = re.sub(r'\d+', '', s)
    d = numbers[0]
    global balance
    balance += d
    bot.reply_to(message, f'Ваш баланс увеличен на: {d}')
    global history
    global NowPos
    global historytext
    history[NowPos] = d
    historytext[NowPos] = text_without_numbers
    NowPos += 1

@bot.message_handler(commands = 'addexpense')
def addexpense( message):
    s = message.text
    symbols_to_remove = "/addexpense  "

    for symbol in symbols_to_remove:
        s = s.replace(symbol, "")

    numbers = [int(x) for x in re.findall(r'\d+', s)]
    text_without_numbers = re.sub(r'\d+', '', s)

    d = numbers[0]
    global balance
    balance -= d
    bot.reply_to(message, f'С вашего баланса снято: {d}')
    global history
    global NowPos
    global historytext
    history[NowPos] = d * -1
    historytext[NowPos] = text_without_numbers
    NowPos += 1

@bot.message_handler(commands = 'balance')
def balance_show( message):
    global balance
    d = balance
    bot.reply_to(message, f'Ваш баланс составляет: {d}')

@bot.message_handler(commands = 'setbudget')
def setbudget( message):
    s = message.text
    symbols_to_remove = "/setbudget  "

    for symbol in symbols_to_remove:
        s = s.replace(symbol, "")

    d = int(s)
    global budget
    budget = d
    bot.reply_to(message, f'Ваш бюджет: {d}')

@bot.message_handler(commands = 'budget')
def budget_show( message):
    global budget
    global balance
    d = budget + balance
    bot.reply_to(message, f'Ваш бюджет составляет: {d}')

@bot.message_handler(commands = 'setgoal')
def setgoal( message):
    s = message.text
    symbols_to_remove = "/setgoal  "

    for symbol in symbols_to_remove:
        s = s.replace(symbol, "")

    numbers = [int(x) for x in re.findall(r'\d+', s)]
    realgoal = numbers[0]
    text_without_numbers = re.sub(r'\d+', '', s )
    global goal
    global goaltext
    goaltext = text_without_numbers
    goal = realgoal
    bot.reply_to(message, f'Поставлена цель: {realgoal} на {text_without_numbers}')

@bot.message_handler(commands = 'goal')
def goal_show( message):
    global goaltext
    if goaltext != "/dQDVSCVdssrg":
        global goal
        global balance
        x = goal - balance
        if x <= 0:
            bot.reply_to(message, f'Вы достигли своей цели в {goal}. \n Можете купить себе {goaltext}.')
        else:
            bot.reply_to(message, f'До вашей цели ({goaltext}, которая стоит {goal} рублей) осталось накопить {x} рублей.')
    else:
        bot.reply_to(message, 'У Вас нет цели.')

@bot.message_handler(commands = 'report')
def report(message):

    s = message.text.replace('/report', '').strip()
    if not s.isdigit():
        bot.reply_to(message, 'Пожалуйста, укажите корректное число операций для отчета.')
        return
    d = int(s)
    if d > NowPos:
        bot.reply_to(message, f'У вас только {NowPos} операций в истории.')
        return
    report_text = "Последние операции:\n"
    for i in range(NowPos - d, NowPos):
        report_text += f'{history[i]} {historytext[i]}\n'

    bot.reply_to(message, report_text)



bot.polling()