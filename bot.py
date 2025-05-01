import openai
import telebot
import os
from collections import defaultdict

# API keys
openai.api_key = 'YOUR_OPENAI_API_KEY'  # Ganti dengan API key OpenAI Anda
TELEGRAM_API_KEY = 'YOUR_TELEGRAM_API_KEY'  # Ganti dengan API key bot Telegram Anda

# Bot setup
bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Penyimpanan untuk limit pertanyaan per user
user_questions = defaultdict(int)  # Menyimpan jumlah pertanyaan per user

# Fungsi untuk memanggil OpenAI API
def get_openai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="gpt-4",  # Atau gpt-3.5-turbo, tergantung kebutuhan
            prompt=prompt,
            max_tokens=1000  # Sesuaikan dengan kebutuhan
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

# Fungsi untuk memeriksa apakah user sudah mencapai batas pertanyaan
def check_question_limit(user_id):
    return user_questions[user_id] < 50  # Batas pertanyaan per user

# Fungsi untuk menangani pesan masuk di Telegram
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    if not check_question_limit(user_id):
        bot.reply_to(message, "Maaf, kamu sudah mencapai batas pertanyaan hari ini.")
        return

    # Meningkatkan jumlah pertanyaan user
    user_questions[user_id] += 1

    # Kirim prompt ke OpenAI dan dapatkan jawaban
    prompt = message.text
    openai_response = get_openai_response(prompt)
    
    # Kirimkan hasil respon ke Telegram user
    bot.reply_to(message, openai_response)

    # Tampilkan status pertanyaan user
    print(f"User {user_name} ({user_id}) bertanya: {prompt}")
    print(f"Respon dari AI: {openai_response}")

# Start bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
