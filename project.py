# Бот переводчик, переводит с русского на английский и со всех на русский.
# Для начала необходимо установить библиотеки
#             pip install googletrans==3.1.0a0  -важно утановить именно эту версию библиотеки
#             pip install pyTelegramBotAPI
#             pip install asyncio
#             pip install aiohttp

# Импорт библиотек:
from googletrans import Translator
from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import InlineQuery, InputTextMessageContent
from telebot import types

# токен бота нужно получить у @BotFather в Телеграме.
bot = AsyncTeleBot("5990015460:AAEEyykgg5tlDTx9V4dZOtx-LMpsFp9SVxw", parse_mode=None)

# Обработка команды /start приветствие.
@bot.message_handler(commands=['start'])
# @bot.message_handler: Это декоратор, который указывает, что функция, к которой он применяется,
# будет обрабатывать определенный тип сообщений в боте.
# # Приветственное сообщение при команде /start
async def send_welcome(message):
    await bot.reply_to(message,'------\n'
                 + 'Здравствуй, '
                 + message.from_user.first_name
                 + ' \nПереведу с русского на английский \n И с других языков на русский '
                 +'\n------')

# Обработка команды /help.
@bot.message_handler(commands=['help'])
 # Помощь при команде /help
async def send_welcome(message):
    await bot.reply_to(message,'------\n'
# Обработка изображений с подписями
                 + 'Просто вводи текст и нажимай отправить\n'
                 + 'Я сам определю какой это язык\n'
                 + 'Если не перевел, попробуй еще раз\n'
                 + 'Перевод гугл'
                 +'\n------')

# Обработка текста сообщения, если ввод на русском, то перевод на английский,
# если другой язык, то перевод на русский.
@bot.message_handler()
# Обработка инлайн запросов


async def user_text(message):
    translator = Translator()

    # Определение языка ввода.
    lang = translator.detect(message.text)
    lang = lang.lang

    # Если ввод по русски, то перевести на английский по умолчанию.
    # Если нужен другой язык, измени <message.text> на <message.text, dest='нужный язык'>.
    if lang == 'ru':
        send = translator.translate(message.text)
        await bot.reply_to(message, '------\n'+ send.text +'\n------')

    # Иначе другой язык перевести на русский {dest='ru'}.
    else:
        send = translator.translate(message.text, dest='ru')
        await bot.reply_to(message, '------\n'+ send.text +'\n------')

# Обработка картинок с подписями
@bot.message_handler(content_types=['photo'])
async def handle_image(message):
    translator = Translator()
    #Обработчик сообщений с изображениями
    chat_id = message.chat.id
    photo = message.photo[-1].file_id
    caption = message.caption

    # Определение языка ввода.
    lang = translator.detect(caption)
    lang = lang.lang

    # Если подпись по русски, то перевести на английский по умолчанию.
    if lang == 'ru':
        send = translator.translate(caption)

    # Иначе другой язык перевести на русский {dest='ru'}.
    else:
        send = translator.translate(caption, dest='ru')
    await bot.send_photo(chat_id, photo, caption=send.text)

# Обработка инлайн запросов. Инлайн режим необходимо включить в настройках бота у @BotFather.
@bot.inline_handler(lambda query: True)
async def inline_query(query):
    results = []
    translator = Translator()
    text = query.query.strip()

    # Если запрос пустой, не делаем перевод
    if not text:
        return

    # Определение языка ввода.
    lang = translator.detect(text)
    lang = lang.lang

    # Если ввод по русски, то перевести на английский по умолчанию.
    if lang == 'ru':
        send = translator.translate(text)
        results.append(types.InlineQueryResultArticle(
            id='1', title=send.text, input_message_content=types.InputTextMessageContent(
                message_text=send.text)))

    # Иначе другой язык перевести на русский {dest='ru'}.
    else:
        send = translator.translate(text, dest='ru')
        results.append(types.InlineQueryResultArticle(
            id='1', title=send.text, input_message_content=types.InputTextMessageContent(
                message_text=send.text)))

    await bot.answer_inline_query(query.id, results)

# Запуск и повторение запуска при сбое.
asyncio.run(bot.infinity_polling())


#send_welcome: Приветствует пользователя при вводе команды /start или /help.
#user_text: Определяет язык введенного текста и переводит его
# с русского на английский (по умолчанию) или с другого языка на русский.
#handle_image: Обрабатывает изображения с подписями, определяет язык подписи и переводит ее.
#inline_query: Обрабатывает инлайн-запросы,
# определяет язык введенного текста и предоставляет результат в виде статьи с переводом.
#Запуск бота: Используется asyncio.run(bot.infinity_polling()) для запуска бота и
# его бесконечного ожидания новых сообщений.
#
