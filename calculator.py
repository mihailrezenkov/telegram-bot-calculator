# calculator.py

import logging
from typing import Dict, Optional, Union, List, Any
from logger import setup_logger, log_error

# Настраиваем логгер для этого модуля
logger = setup_logger(__name__)


def calc(expression: str) -> str:
    """
    Принимает математическое выражение словами, возвращает результат словами
    
    Args:
        expression: Строка с математическим выражением (на русском языке)
    
    Returns:
        str: Результат вычисления или сообщение об ошибке
    
    Examples:
        >>> calc("два плюс два")
        'четыре'
        >>> calc("десять минус пять")
        'пять'
    """
    
    logger.info(f"Получено выражение: {expression}")
    
    try:
        # Словари для преобразования чисел
        small_digits: Dict[str, int] = {
            'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5, 
            'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9
        }
        
        unique_digits: Dict[str, int] = {
            'ноль': 0, 'десять': 10, 'одиннадцать': 11, 'двенадцать': 12,
            'тринадцать': 13, 'четырнадцать': 14, 'пятнадцать': 15,
            'шестнадцать': 16, 'семнадцать': 17, 'восемнадцать': 18,
            'девятнадцать': 19
        }
        
        big_digits: Dict[str, int] = {
            'двадцать': 20, 'тридцать': 30, 'сорок': 40, 'пятьдесят': 50,
            'шестьдесят': 60, 'семьдесят': 70, 'восемьдесят': 80,
            'девяносто': 90
        }
        
        large_digits: Dict[str, int] = {
            'сто': 100, 'двести': 200, 'триста': 300, 'четыреста': 400, 
            'пятьсот': 500, 'шестьсот': 600, 'семьсот': 700, 'восемьсот': 800,
            'девятьсот': 900
        }
        
        super_large_digits: Dict[str, int] = {
            'тысяча': 1000, 'две тысячи': 2000, 'три тысячи': 3000, 
            'четыре тысячи': 4000, 'пять тысяч': 5000,
            'шесть тысяч': 6000, 'семь тысяч': 7000, 'восемь тысяч': 8000,
            'девять тысяч': 9000
        }

        all_digits: Dict[str, int] = {
            **small_digits, **unique_digits, **big_digits, **large_digits
        }

        operators: Dict[str, str] = {
            'плюс': '+', 'минус': '-', 'умножить на': '*', 
            'скобка открывается': '(', 'скобка закрывается': ')'
        }

        sign: str = ''
        
        # Приводим к нижнему регистру и убираем пробелы по краям
        expression = expression.lower().strip()

        # Заменяем операторы
        for name, operator in operators.items():
            expression = expression.replace(name, operator)

        # Проверяем наличие операторов
        if '-' not in expression and '+' not in expression and '*' not in expression:
            logger.warning(f"В выражении нет операторов: {expression}")
            return 'В выражении нет поддерживаемых операторов'
        
        # Разбиваем на числа
        nums_expression: str = expression
        for name, operator in operators.items():
            nums_expression = nums_expression.replace(operator, '=')
            
        nums_expression_list: List[str] = nums_expression.split('=')
        
        for i in range(len(nums_expression_list)):
            nums_expression_list[i] = nums_expression_list[i].strip()
        
        # Удаляем пустые строки
        while '' in nums_expression_list:
            nums_expression_list.remove('')

        def clear(n: str) -> Optional[int]:
            """
            Преобразует слово/слова в число
            
            Args:
                n: Строка с числом словами
            
            Returns:
                Optional[int]: Число или None если ошибка
            """
            n = n.strip()
            if ' ' in n:
                parts: List[str] = n.split()
                if len(parts) == 2:
                    n1, n2 = parts
                    
                    if n1 not in big_digits:
                        logger.warning(f"Неизвестное число: {n1}")
                        return None
                    if n2 not in small_digits:
                        logger.warning(f"Неизвестное число: {n2}")
                        return None
                    result: int = all_digits[n1] + all_digits[n2]
                    return result
            else:
                if n not in all_digits:
                    logger.warning(f"Неизвестное число: {n}")
                    return None
                return all_digits[n]
            return None
            
        # Обрабатываем числа в выражении
        for i in nums_expression_list:
            clear_result: Optional[int] = clear(i)
            if clear_result is None:
                logger.warning(f"Ошибка в числе: {i}")
                return 'В выражении ошибка'
            expression = expression.replace(i, str(clear_result), 1)
        
        # Вычисляем
        try:
            n: Union[int, float] = eval(expression)
            logger.debug(f"Результат вычисления: {n}")
        except ZeroDivisionError:
            logger.error("Деление на ноль")
            return 'Ошибка: деление на ноль!'
        except Exception as e:
            log_error(logger, e, "Ошибка при вычислении")
            return f'Ошибка в выражении: {str(e)}'

        # Конвертируем результат обратно в слова
        if n < 0:
            sign = 'минус'
            n = abs(n)
        
        # Проверяем целое ли число
        if isinstance(n, float):
            if n.is_integer():
                n = int(n)
            else:
                result_str: str = f'{sign} {n}'.strip()
                logger.info(f"Результат (дробное): {result_str}")
                return result_str
        
        # Преобразуем число обратно в слова
        result_words: str = _number_to_words(n, sign, all_digits, small_digits, unique_digits, 
                                            big_digits, large_digits, super_large_digits)
        logger.info(f"Результат: {result_words}")
        return result_words
        
    except Exception as e:
        log_error(logger, e, "Критическая ошибка в калькуляторе")
        return f'Внутренняя ошибка калькулятора: {str(e)}'


def _number_to_words(n: int, sign: str, all_digits: Dict[str, int], 
                     small_digits: Dict[str, int], unique_digits: Dict[str, int],
                     big_digits: Dict[str, int], large_digits: Dict[str, int],
                     super_large_digits: Dict[str, int]) -> str:
    """
    Вспомогательная функция для преобразования числа в слова
    
    Args:
        n: Число для преобразования
        sign: Знак ('минус' или '')
        all_digits: Общий словарь чисел
        small_digits: Словарь чисел 1-9
        unique_digits: Словарь особых чисел
        big_digits: Словарь десятков
        large_digits: Словарь сотен
        super_large_digits: Словарь тысяч
    
    Returns:
        str: Число словами
    """
    
    # Проверяем простые числа
    if n in small_digits or n in unique_digits:
        for name, value in all_digits.items():
            if n == value:
                return sign + ' ' + name
    
    # Двузначные числа
    if len(str(n)) == 2:
        n1, n2 = int(str(n)[0]), int(str(n)[-1])
        for name, value in all_digits.items():
            if n1*10 == value:
                n1_name = name
                break
        else:
            n1_name = ''
        
        n2_name = ''
        if n2 != 0:
            for name, value in all_digits.items():
                if n2 == value:
                    n2_name = name
                    break
        
        result = sign + ' ' + n1_name + ' ' + n2_name
        return result.strip()
    
    # Трехзначные числа
    if len(str(n)) == 3:
        n1, n2, n3 = int(str(n)[0]), int(str(n)[-2]), int(str(n)[-1])
        
        for name, value in large_digits.items():
            if n1*100 == value:
                n1_name = name
                break
        else:
            n1_name = ''
        
        n2_name = ''
        if n2 != 0:
            for name, value in all_digits.items():
                if n2*10 == value:
                    n2_name = name
                    break
        
        n3_name = ''
        if n3 != 0:
            for name, value in all_digits.items():
                if n3 == value:
                    n3_name = name
                    break
        
        result = sign + ' ' + n1_name + ' ' + n2_name + ' ' + n3_name
        return result.strip()
    
    # Четырехзначные числа
    if len(str(n)) == 4:
        n1, n2, n3, n4 = int(str(n)[0]), int(str(n)[-3]), int(str(n)[-2]), int(str(n)[-1])
        
        for name, value in super_large_digits.items():
            if n1*1000 == value:
                n1_name = name
                break
        else:
            n1_name = ''
        
        n2_name = ''
        if n2 != 0:
            for name, value in all_digits.items():
                if n2*100 == value:
                    n2_name = name
                    break
        
        n3_name = ''
        if n3 != 0:
            for name, value in all_digits.items():
                if n3*10 == value:
                    n3_name = name
                    break
        
        n4_name = ''
        if n4 != 0:
            for name, value in all_digits.items():
                if n4 == value:
                    n4_name = name
                    break
        
        result = sign + ' ' + n1_name + ' ' + n2_name + ' ' + n3_name + ' ' + n4_name
        return result.strip()
    
    # Если число не подходит ни под один формат
    return str(n)


# Для тестирования (работает только при прямом запуске)
if __name__ == '__main__':
    logger.info("Запуск калькулятора в режиме тестирования")
    while True:
        user_input: str = input("Введите выражение (или 'exit' для выхода): ")
        if user_input.lower() == 'exit':
            break
        result: str = calc(user_input)
        print(result.strip())