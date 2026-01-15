import telebot
from telebot import types

# ====== CONFIG ======
TOKEN = "TOKEN"  # Saka token dinka nan
ADMIN_ID = 6648308251      # Saka Telegram ID ɗinka nan

bot = telebot.TeleBot(TOKEN)

# ====== Users score tracker ======
users_scores = {}

# ====== Lessons placeholders ======
lessons = {
    "Physics": ["Lesson 1", "Lesson 2", "Lesson 3"],
    "Math": ["Lesson 1", "Lesson 2", "Lesson 3"],
    "Chemistry": ["Lesson 1", "Lesson 2", "Lesson 3"]
}

# ====== Socials / About URLs ======
socials = {
    "Telegram": "https://t.me/Mahmudsm1",
    "Facebook": "https://www.facebook.com/share/1aVMXfbxQY/",
    "X": "https://x.com/Mahmud_sm1"
}

# ====== Broadcast buffer ======
broadcast_buffer = {}

# ====== Start Command ======
@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    users_scores[chat_id] = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Lessons", "About")
    markup.row("Socials", "Broadcast")  # Broadcast only for admin
    bot.send_message(chat_id, "Welcome! Choose an option:", reply_markup=markup)

# ====== Text Handlers ======
@bot.message_handler(func=lambda m: True)
def menu_handler(message):
    chat_id = message.chat.id
    text = message.text

    if text == "Lessons":
        show_subjects(chat_id)
    elif text == "About":
        about_text = (
            "This bot helps you explore different lessons and track your progress.\n"
            "For more info, contact @MHSM5 on Telegram."
        )
        bot.send_message(chat_id, about_text)
    elif text == "Socials":
        show_socials(chat_id)
    elif text == "Broadcast":
        if chat_id == ADMIN_ID:
            msg = bot.send_message(chat_id, "Type the message you want to broadcast:")
            bot.register_next_step_handler(msg, do_broadcast)
        else:
            bot.send_message(chat_id, "You are not authorized to use this.")
    else:
        bot.send_message(chat_id, "Choose a valid option.")

# ====== Lessons Menu ======
def show_subjects(chat_id):
    markup = types.InlineKeyboardMarkup()
    for subject in lessons.keys():
        markup.add(types.InlineKeyboardButton(subject, callback_data=f"subject:{subject}"))
    bot.send_message(chat_id, "Select a subject:", reply_markup=markup)

def show_lessons(chat_id, subject):
    markup = types.InlineKeyboardMarkup()
    for lesson in lessons[subject]:
        markup.add(types.InlineKeyboardButton(lesson, callback_data=f"lesson:{subject}:{lesson}"))
    bot.send_message(chat_id, f"Select a lesson from {subject}:", reply_markup=markup)

# ====== Socials Menu ======
def show_socials(chat_id):
    markup = types.InlineKeyboardMarkup()
    for name, url in socials.items():
        markup.add(types.InlineKeyboardButton(name, url=url))
    bot.send_message(chat_id, "Follow me on:", reply_markup=markup)

# ====== Callback Query Handler ======
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("subject:"):
        subject = data.split(":")[1]
        show_lessons(chat_id, subject)
    elif data.startswith("lesson:"):
        parts = data.split(":")
        subject = parts[1]
        lesson = parts[2]
        # Placeholder for sending PDF or lesson content
        bot.send_message(chat_id, f"You selected {lesson} of {subject}. (PDFs not included)")
        # Increment score
        users_scores[chat_id] += 1
        bot.send_message(chat_id, f"Your current score: {users_scores[chat_id]} ✅")

# ====== Broadcast Handler ======
def do_broadcast(message):
    if message.chat.id != ADMIN_ID:
        return
    text = message.text
    # Send to all users in users_scores
    for user_id in users_scores.keys():
        try:
            bot.send_message(user_id, f"📢 Broadcast:\n{text}")
        except Exception:
            pass
    bot.send_message(ADMIN_ID, "Broadcast sent to all users.")

# ====== Run Bot ======
bot.infinity_polling()
