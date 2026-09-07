# main.py

from bot import run_bot
from logger import setup_logger

# Настраиваем логгер для главного модуля
logger = setup_logger(__name__)


if __name__ == '__main__':
    """
    Точка входа в программу
    """
    try:
        logger.info("=" * 50)
        logger.info("Запуск приложения...")
        run_bot()
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        raise