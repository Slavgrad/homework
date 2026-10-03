"""
Тесты для homeworks/hw01_lecture1/hw01.py

Запуск локально (из корня репозитория):

    pytest tests/hw01 -v

Этот же набор тестов запускает GitHub Actions при каждом push и
pull request – см. .github/workflows/homework-check.yml.
"""

from decimal import Decimal
from fractions import Fraction

import pytest

from homeworks.hw01_lecture1.hw01 import (
    active_flags,
    add_to_log,
    complex_magnitudes,
    count_passing,
    exact_sum,
    filter_out_none,
    floor_and_truncated_division,
    independent_copy,
    round_money,
    to_all_bases,
)


class AlwaysEqual:
    def __eq__(self, other):
        return True


# Задание 1 -------------------------------------------------------------
def test_add_to_log_basic():
    assert add_to_log('a') == ['a']


def test_add_to_log_default_not_shared():
    first = add_to_log('a')
    second = add_to_log('b')
    assert first == ['a']
    assert second == ['b']


def test_add_to_log_explicit_log():
    log = ['x']
    assert add_to_log('y', log) == ['x', 'y']


def test_add_to_log_accumulates_on_shared_explicit_log():
    log = []
    add_to_log('a', log)
    add_to_log('b', log)
    assert log == ['a', 'b']


# Задание 2 -------------------------------------------------------------
def test_exact_sum_thirds():
    assert exact_sum(['1/3', '1/3', '1/3']) == Fraction(1, 1)


def test_exact_sum_mixed_forms():
    assert exact_sum(['0.1', '0.2']) == Fraction(3, 10)


def test_exact_sum_returns_fraction_type():
    assert isinstance(exact_sum(['1', '2']), Fraction)


def test_exact_sum_empty_list():
    assert exact_sum([]) == Fraction(0)


def test_exact_sum_negative_values():
    assert exact_sum(['-2/5', '1/5']) == Fraction(-1, 5)


# Задание 3 -------------------------------------------------------------
def test_round_money_half_up():
    assert round_money(2.675, 2) == Decimal('2.68')


def test_round_money_integer_amount():
    assert round_money(10, 2) == Decimal('10.00')


def test_round_money_string_input():
    assert round_money('19.995', 2) == Decimal('20.00')


def test_round_money_returns_decimal():
    assert isinstance(round_money(1, 2), Decimal)


def test_round_money_negative_amount():
    assert round_money(-2.675, 2) == Decimal('-2.68')


def test_round_money_zero_places():
    assert round_money(5.5, 0) == Decimal('6')


# Задание 4 -------------------------------------------------------------
def test_active_flags_basic():
    names = ['read', 'write', 'execute', 'delete']
    assert active_flags(0b1010, names) == ['write', 'delete']


def test_active_flags_all_set():
    assert active_flags(0b111, ['a', 'b', 'c']) == ['a', 'b', 'c']


def test_active_flags_none_set():
    assert active_flags(0, ['a', 'b', 'c']) == []


def test_active_flags_ignores_bits_without_names():
    # бит 4 установлен, но names описывает только биты 0-2 – лишний
    # бит не должен приводить ни к ошибке, ни к лишнему элементу.
    assert active_flags(0b10001, ['a', 'b', 'c']) == ['a']


# Задание 5 -------------------------------------------------------------
def test_independent_copy_equal_value():
    matrix = [[1, [2, 3]], [4, 5]]
    assert independent_copy(matrix) == matrix


def test_independent_copy_empty_list():
    assert independent_copy([]) == []


def test_independent_copy_not_same_object():
    matrix = [[1, [2, 3]], [4, 5]]
    cp = independent_copy(matrix)
    assert cp is not matrix


def test_independent_copy_deep_independence():
    matrix = [[1, [2, 3]], [4, 5]]
    cp = independent_copy(matrix)
    cp[0][1].append(99)
    assert matrix == [[1, [2, 3]], [4, 5]]
    assert cp == [[1, [2, 3, 99]], [4, 5]]


# Задание 6 -------------------------------------------------------------
def test_complex_magnitudes_basic():
    assert complex_magnitudes([3 + 4j, 1 + 1j, 0j]) == [5.0, 1.41, 0.0]


def test_complex_magnitudes_returns_list_of_floats():
    result = complex_magnitudes([2j])
    assert result == [2.0]
    assert isinstance(result[0], float)


def test_complex_magnitudes_empty_list():
    assert complex_magnitudes([]) == []


# Задание 7 -------------------------------------------------------------
def test_count_passing_basic():
    assert count_passing([55, 90, 61, 40, 88], 60) == 3


def test_count_passing_none_pass():
    assert count_passing([10, 20, 30], 100) == 0


def test_count_passing_all_pass():
    assert count_passing([10, 20, 30], 5) == 3


def test_count_passing_empty_scores():
    assert count_passing([], 50) == 0


def test_count_passing_boundary_equal_to_threshold():
    # >= threshold, а не > threshold – граница включена
    assert count_passing([60], 60) == 1


# Задание 8 -------------------------------------------------------------
def test_to_all_bases_positive():
    assert to_all_bases(42) == ('0b101010', '0x2a', '0o52')


def test_to_all_bases_negative():
    assert to_all_bases(-10) == ('-0b1010', '-0xa', '-0o12')


def test_to_all_bases_zero():
    assert to_all_bases(0) == ('0b0', '0x0', '0o0')


# Задание 9 -------------------------------------------------------------
@pytest.mark.parametrize('a,b,expected', [
    (7, 2, (3, 3)),
    (-7, 2, (-4, -3)),
    (7, -2, (-4, -3)),
    (-7, -2, (3, 3)),
    (8, 2, (4, 4)),      # делится без остатка – floor и truncated совпадают
    (-8, 2, (-4, -4)),   # то же самое, но с отрицательным делимым
])
def test_floor_and_truncated_division(a, b, expected):
    assert floor_and_truncated_division(a, b) == expected


# Задание 10 -------------------------------------------------------------
def test_filter_out_none_removes_none():
    assert filter_out_none([1, None, 2, None, 3]) == [1, 2, 3]


def test_filter_out_none_keeps_always_equal_object():
    weird = AlwaysEqual()
    values = [1, None, weird, 2, None]
    result = filter_out_none(values)
    assert len(result) == 3
    assert any(item is weird for item in result)
    assert not any(item is None for item in result)


def test_filter_out_none_empty_list():
    assert filter_out_none([]) == []


def test_filter_out_none_no_none_present():
    assert filter_out_none([1, 2, 3]) == [1, 2, 3]
