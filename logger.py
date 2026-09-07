import logging
import sys
from typing import Optional


def setup_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Настройка логгера с единым форматом
    
    Args:
        name: Имя логгера (если None - возвращает root logger)
        level: Уровень логирования
    
    Returns:
        logging.Logger: Настроенный логгер
    """
    logger = logging.getLogger(name) if name else logging.getLogger()
    
    # Устанавливаем уровень логирования
    logger.setLevel(level)
    
    # Создаем обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Формат логов: время - имя - уровень - сообщение
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Добавляем обработчик к логгеру (если еще нет)
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger


def log_error(logger: logging.Logger, error: Exception, context: str = "") -> None:
    """
    Универсальная функция для логирования ошибок
    
    Args:
        logger: Экземпляр логгера
        error: Объект исключения
        context: Дополнительный контекст ошибки
    """
    if context:
        logger.error(f"{context}: {str(error)}", exc_info=True)
    else:
        logger.error(f"{str(error)}", exc_info=True)