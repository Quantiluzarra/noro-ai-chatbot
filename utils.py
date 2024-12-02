import logging
from datetime import datetime

class BotLogger:
    @staticmethod
    def log_interaction(user_id, message):
        log_entry = f"{datetime.now()} - User {user_id}: {message}\n"
        with open('interactions.log', 'a') as log_file:
            log_file.write(log_entry)
    
    @staticmethod
    def log_error(error):
        logging.error(f"{datetime.now()} - ERROR: {error}")

class SecurityManager:
    @staticmethod
    def validate_message(message):
        # Базовая фильтрация сообщений
        forbidden_words = ['мат', 'оскорбление']
        return not any(word in message.lower() for word in forbidden_words)
