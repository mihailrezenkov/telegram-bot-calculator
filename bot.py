# bot.py

import logging
from typing import Optional
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, help_command, handle_message, unknown
from config import TOKEN, BOT_NAME, BOT_VERSION, LOG_LEVEL
from logger import setup_logger, log_error

# Настраиваем логгер для этого модуля
logger = setup_logger(__name__)


def run_bot() -> None:
    """
    Запускает Telegram бота
    """
    try:
        logger.info(f"🚀 Запуск {BOT_NAME} v{BOT_VERSION}...")
        logger.info(f"Уровень логирования: {LOG_LEVEL}")
        
        # Создаем приложение
        application = ApplicationBuilder().token(TOKEN).build()
        logger.info("Приложение создано")
        
        # Регистрируем команды
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        
        # Регистрируем обработчик ВСЕХ текстовых сообщений (кроме команд)
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            handle_message
        ))
        
        # Обработчик для неизвестных команд
        application.add_handler(MessageHandler(
            filters.COMMAND, 
            unknown
        ))
        
        logger.info("✅ Все обработчики зарегистрированы")
        logger.info("🤖 Бот запущен! Нажми Ctrl+C для остановки.")
        
        # Запускаем бота
        application.run_polling()
        
    except Exception as e:
        log_error(logger, e, "Критическая ошибка при запуске бота")
        raise