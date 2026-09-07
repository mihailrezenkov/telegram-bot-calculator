# handlers.py

import logging
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
from calculator import calc
from logger import setup_logger, log_error

# Настраиваем логгер для этого модуля
logger = setup_logger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start
    
    Args:
        update: Объект обновления от Telegram
        context: Контекст обработчика
    """
    try:
        user_name: str = update.effective_user.first_name if update.effective_user else "Пользователь"
        user_id: int = update.effective_user.id if update.effective_user else 0
        
        logger.info(f"Пользователь {user_id} ({user_name}) запустил бота")
        
        await update.message.reply_text(
            f"🧮 Привет, {user_name}!\n\n"
            "Я бот-калькулятор. Я понимаю математические выражения словами.\n\n"
            "📝 **Примеры:**\n"
            "• два плюс два\n"
            "• пять умножить на три\n"
            "• скобка открывается три плюс пять скобка закрывается умножить на два\n"
            "• двадцать пять минус десять\n\n"
            "Отправь /help для полной справки.",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        log_error(logger, e, f"Ошибка в обработчике start для пользователя {update.effective_user.id if update.effective_user else 'unknown'}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуй позже.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /help
    
    Args:
        update: Объект обновления от Telegram
        context: Контекст обработчика
    """
    try:
        user_id: int = update.effective_user.id if update.effective_user else 0
        logger.info(f"Пользователь {user_id} запросил справку")
        
        await update.message.reply_text(
            "📖 **Как пользоваться ботом:**\n\n"
            "Просто напиши математическое выражение словами.\n\n"
            "**Поддерживаемые операторы:**\n"
            "• плюс → +\n"
            "• минус → -\n"
            "• умножить на → *\n"
            "• скобка открывается → (\n"
            "• скобка закрывается → )\n\n"
            "**Числа:**\n"
            "• от нуля до девяти (один, два, три...)\n"
            "• от десяти до девятнадцати (десять, одиннадцать...)\n"
            "• десятки (двадцать, тридцать...)\n"
            "• сотни (сто, двести...)\n"
            "• тысячи (тысяча, две тысячи...)\n\n"
            "**Примеры:**\n"
            "• `два плюс два` → четыре\n"
            "• `пять умножить на три` → пятнадцать\n"
            "• `скобка открывается три плюс пять скобка закрывается умножить на два` → шестнадцать\n"
            "• `двадцать пять минус десять` → пятнадцать",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        log_error(logger, e, f"Ошибка в обработчике help для пользователя {update.effective_user.id if update.effective_user else 'unknown'}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуй позже.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик всех текстовых сообщений
    
    Args:
        update: Объект обновления от Telegram
        context: Контекст обработчика
    """
    try:
        user_id: int = update.effective_user.id if update.effective_user else 0
        user_text: str = update.message.text if update.message else ""
        
        logger.info(f"Пользователь {user_id} отправил: {user_text}")
        
        # Вызываем функцию калькулятора
        result: str = calc(user_text)
        
        # Отправляем результат пользователю
        await update.message.reply_text(
            f"🧮 **Результат:**\n{result.strip()}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Пользователю {user_id} отправлен результат: {result}")
        
    except Exception as e:
        log_error(logger, e, f"Ошибка в обработчике сообщения от пользователя {update.effective_user.id if update.effective_user else 'unknown'}")
        await update.message.reply_text("❌ Произошла ошибка при обработке запроса. Попробуй еще раз.")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик неизвестных команд
    
    Args:
        update: Объект обновления от Telegram
        context: Контекст обработчика
    """
    try:
        user_id: int = update.effective_user.id if update.effective_user else 0
        command: str = update.message.text if update.message else "unknown"
        
        logger.warning(f"Пользователь {user_id} ввел неизвестную команду: {command}")
        
        await update.message.reply_text(
            "🤔 Неизвестная команда.\n"
            "Используй /help для списка команд."
        )
        
    except Exception as e:
        log_error(logger, e, "Ошибка в обработчике неизвестной команды")