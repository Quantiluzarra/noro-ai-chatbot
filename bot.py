import telebot
import nltk
from nltk.chat.util import Chat, reflections
import random
from transformers import pipeline

class NoroAIBot:
    def __init__(self, token):
        self.token = token
        self.bot = telebot.TeleBot(token)
        
        # Разработчики
        self.developers = [
            "Noro Laboratory+", 
            "Noro Laboratory Ats"
        ]
        
        # Базовые паттерны ответов
        self.patterns = [
            [
                r'привет|здравствуй|hi|hello',
                ['Привет! Чем могу помочь?', 'Здравствуйте!']
            ],
            [
                r'кто тебя создал|кто разработчик',
                [f'Меня создали {", ".join(self.developers)}']
            ],
            [
                r'как дела\?',
                ['Отлично! Готов помочь', 'Всё хорошо, спасибо!']
            ]
        ]
        
        # Инициализация чат-модели
        self.chatbot = Chat(self.patterns, reflections)
        
        # Генератор текста
        self.text_generator = pipeline('text-generation', model='gpt2')
        
        # Регистрация обработчиков
        self.register_handlers()
    
    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            welcome_text = f"Привет! Я бот от {', '.join(self.developers)}"
            self.bot.reply_to(message, welcome_text)
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            user_text = message.text.lower()
            
            # Проверка на разработчиков
            if any(dev.lower() in user_text for dev in self.developers):
                response = f"Да, я знаю {', '.join(self.developers)}. Они мои создатели!"
            else:
                # Попытка ответить через встроенные паттерны
                chat_response = self.chatbot.respond(user_text)
                
                # Если нет готового ответа - генерация
                if not chat_response:
                    try:
                        generated = self.text_generator(user_text, max_length=50)[0]['generated_text']
                        response = generated
                    except:
                        response = "Извините, я не понял вас. Можете перефразировать?"
                else:
                    response = chat_response
            
            self.bot.reply_to(message, response)
    
    def start(self):
        print("Бот Noro Laboratory запущен...")
        self.bot.polling()

# Токен бота
BOT_TOKEN = "8185421413:AAE4hMfApL40d-Dw1WjNadI3ck6kPI1sVcU"

if __name__ == "__main__":
    bot = NoroAIBot(BOT_TOKEN)
    bot.start()
