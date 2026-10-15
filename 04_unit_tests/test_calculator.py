# test_calculator.py
"""
Юнит-тесты для калькулятора.
Демонстрируют: параметризацию, проверку исключений, граничные значения.
"""

import pytest
from calculator import (
    add, subtract, multiply, divide, is_even, factorial
)


class TestArithmetic:
    """Тесты базовых операций."""

    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, -50, 50),
        (2.5, 2.5, 5.0),
    ])
    def test_add(self, a, b, expected):
        assert add(a, b) == expected

    @pytest.mark.parametrize("a, b, expected", [
        (5, 3, 2),
        (0, 5, -5),
        (-5, -3, -2),
    ])
    def test_subtract(self, a, b, expected):
        assert subtract(a, b) == expected

    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 6),
        (0, 100, 0),
        (-2, 3, -6),
    ])
    def test_multiply(self, a, b, expected):
        assert multiply(a, b) == expected

    @pytest.mark.parametrize("a, b, expected", [
        (10, 2, 5),
        (9, 3, 3),
        (-10, 2, -5),
    ])
    def test_divide(self, a, b, expected):
        assert divide(a, b) == expected

    def test_divide_by_zero(self):
        """Граничный случай: деление на ноль."""
        with pytest.raises(ValueError, match="Деление на ноль"):
            divide(10, 0)


class TestParity:
    """Тесты чётности."""

    @pytest.mark.parametrize("n, expected", [
        (2, True),
        (3, False),
        (0, True),
        (-4, True),
        (-3, False),
    ])
    def test_is_even(self, n, expected):
        assert is_even(n) == expected


class TestFactorial:
    """Тесты факториала."""

    @pytest.mark.parametrize("n, expected", [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800),
    ])
    def test_factorial_positive(self, n, expected):
        assert factorial(n) == expected

    def test_factorial_negative(self):
        """Граничный случай: отрицательное число."""
        with pytest.raises(ValueError, match="отрицательного"):
            factorial(-1)