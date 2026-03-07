from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *


async def start(update,context):
    dialog.main = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        "start":"Главное меню бота",
        "profile": "генерация Tinder-профля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt":"задать вопрос чату GPT 🧠",
    })


async def gpt(update, context):
    dialog.main = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)


async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question( prompt ,text)
    await send_text(update, context, answer)


async def date(update, context):
    dialog.main = "date"
    text = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, {
        "date_grande":"Ариана Гранде",
        "date_robbie":"Марго Робби",
        "date_zendaya":"Зендея",
        "date gosling":"Райан Гослинг",
        "date_hardy":"Том Харди"
    })


async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "Девушка набирает текст...")
    answer = await chatgpt.add_message(text)
    my_message.edit_text(answer)



async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update, context, query)
    await send_text(update, context, "Отличный выбор! Пригласите девушку (парня) на свидание за 5 сообщений")

    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)

async def message(update, context):
    dialog.mode = "message"
    text = load_message("message")
    await send_photo(update, context, "message")
    await send_text_buttons (update, context, text, {
        "message_next":"Следующее сообщение",
        "message_date":"Пригласить на свидание"
    })
    dialog.list.clear()


async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)
    my_message = await send_text(update, context, "ChatGPT 🧠 думает над вариантами ответ...")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)


async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


async def profile(update, context):
    dialog.mode = "profile"
    text = load_message("profile")
    await send_photo(update, context, "profile")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "Сколько вам лет?")


async def profile_dialog(update, context):
    text = update.message.text
    dialog.count +=1

    if dialog.count == 1:
       dialog.user["age"] = text
       await send_text(update, context, "Кем вы работаете?")
    elif dialog.count == 2:
       dialog.user["occupation"] = text
       await send_text(update, context, "У вас есть хобби?")
    elif dialog.count == 3:
       dialog.user["hobby"] = text
       await send_text(update, context, "Что вам НЕ нравится в людях?")
    elif dialog.count == 4:
       dialog.user["annoys"] = text
       await send_text(update, context, "Цели знакомства?")
    elif dialog.count == 5:
       dialog.user["goals"] = text
       prompt = load_prompt("profile")
       user_info = dialog_user_info_to_str(dialog.user)

       my_message = await send_text(update, context, "ChatGPT 🧠 занимается с генерацией вашего профиля. Подождите пару секунд...")
       answer = await chatgpt.send_question(prompt, user_info)
       await my_message.edit_text(answer)

async def opener(update, context):
    dialog.mode = "opener"
    text = load_message("opener")
    await send_photo(update, context, "opener")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "Имя девушки?")

async def opener_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["name"] = text
        await send_text(update, context, "Сколько ей лет?")
    elif dialog.count == 2:
        dialog.user["age"] = text
        await send_text(update, context, "Оцените её внешность: 1-10 баллов?")
    elif dialog.count == 3:
        dialog.user["handsome"] = text
        await send_text(update, context, "Кем она работает?")
    elif dialog.count == 4:
        dialog.user["occupation"] = text
        await send_text(update, context, "Цели знакомства?")
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("opener")
        user_info = dialog_user_info_to_str(dialog.user)

        answer = await chatgpt.send_question(prompt, user_info)
        await send_text(update, context, answer)



async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    elif dialog.mode == "date":
        await date_dialog(update, context)
    elif dialog.mode == "message":
        await message_dialog(update, context)
    elif dialog.mode == "profile":
        await profile_dialog(update, context)
    elif dialog.mode == "opener":
        await opener_dialog(update, context)
    else:
        await send_text(update, context,"*Привет*")
        await send_text(update, context, "_Как дела?_")
        await send_text(update, context, "Вы написали" + update.message.text)

        await send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, "Запустить процесс?", {
           "start":"Запустить",
           "stop":"Остановить"
        })



async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, "Процесс запущен")
    else:
        await send_text(update, context, "Процесс остановлен")


dialog = Dialog()
dialog.mode = None
dialog.list= []
dialog.count= 0
dialog.user = {}

chatgpt = ChatGptService(token=your-openai-api-key)

app = ApplicationBuilder().token("TELEGRAM_TOKEN=123456789:ABCDEF-your-token-example").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("opener", opener))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="^message_.*"))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
