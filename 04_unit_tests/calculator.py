# calculator.py — простой калькулятор для тестирования

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b

def is_even(n):
    return n % 2 == 0

def factorial(n):
    if n < 0:
        raise ValueError("Факториал отрицательного числа не определён")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result