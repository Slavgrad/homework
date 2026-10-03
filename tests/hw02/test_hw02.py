"""
Тесты для homeworks/hw02_lecture2/hw02.py

Запуск локально (из корня репозитория):

    pytest tests/hw02 -v

Этот же набор тестов запускает GitHub Actions при каждом push и
pull request – см. .github/workflows/homework-check.yml.
"""

import ast
import inspect

import pytest

from homeworks.hw02_lecture2.hw02 import (
    calculate,
    common_words,
    first_n_odd,
    format_report,
    group_by_length,
    moving_average,
    normalize_tokens,
    save_and_load_json,
    top_k,
    word_frequencies,
    write_read_csv,
)


# Задание 1 -------------------------------------------------------------
def test_format_report_basic():
    rows = [('accuracy', 0.87654), ('loss', 0.12345)]
    expected = 'accuracy  : 0.8765\nloss      : 0.1235'
    assert format_report(rows) == expected


def test_format_report_no_trailing_newline():
    assert not format_report([('x', 1.0)]).endswith('\n')


def test_format_report_empty_rows():
    assert format_report([]) == ''


# Задание 2 -------------------------------------------------------------
def test_normalize_tokens_dedup_and_order():
    assert normalize_tokens('кот, кот и пёс! кот.') == ['кот', 'и', 'пёс']


def test_normalize_tokens_lowercase_and_punctuation():
    text = 'The cat, the CAT and the dog! The cat.'
    assert normalize_tokens(text) == ['the', 'cat', 'and', 'dog']


def test_normalize_tokens_empty_string():
    assert normalize_tokens('') == []


def test_normalize_tokens_only_punctuation():
    assert normalize_tokens('...  !!!  ,,,') == []


# Задание 3 -------------------------------------------------------------
def test_top_k_basic():
    scores = [('resnet', 0.91), ('vit', 0.94), ('mlp', 0.78)]
    assert top_k(scores, 2) == [('vit', 0.94), ('resnet', 0.91)]


def test_top_k_zero():
    scores = [('a', 1), ('b', 2)]
    assert top_k(scores, 0) == []


def test_top_k_negative():
    scores = [('a', 1), ('b', 2)]
    assert top_k(scores, -1) == []


def test_top_k_more_than_available():
    scores = [('resnet', 0.91), ('vit', 0.94), ('mlp', 0.78)]
    assert top_k(scores, 10) == [('vit', 0.94), ('resnet', 0.91), ('mlp', 0.78)]


# Задание 4 -------------------------------------------------------------
def test_group_by_length_basic():
    tokens = 'the cat and the dog and the bird'.split()
    expected = {
        3: ['the', 'cat', 'and', 'the', 'dog', 'and', 'the'],
        4: ['bird'],
    }
    assert group_by_length(tokens) == expected


def test_group_by_length_empty():
    assert group_by_length([]) == {}


# Задание 5 -------------------------------------------------------------
def test_word_frequencies_basic():
    assert word_frequencies('the cat and the dog and the bird') == {
        'the': 3, 'cat': 1, 'and': 2, 'dog': 1, 'bird': 1,
    }


def test_common_words_intersection():
    freq_a = word_frequencies('a b b c')
    freq_b = word_frequencies('b c c d')
    assert common_words(freq_a, freq_b) == {'b', 'c'}


def test_word_frequencies_empty_text():
    assert word_frequencies('') == {}


def test_common_words_no_overlap():
    freq_a = word_frequencies('a b')
    freq_b = word_frequencies('c d')
    assert common_words(freq_a, freq_b) == set()


# Задание 6 -------------------------------------------------------------
def test_save_and_load_json_round_trip(tmp_path):
    data = {'a': (1, 2, 3), 1: 'one'}
    path = tmp_path / 'data.json'
    result = save_and_load_json(data, path)
    assert result == {'a': [1, 2, 3], '1': 'one'}
    assert path.exists()


def test_save_and_load_json_indent(tmp_path):
    path = tmp_path / 'data.json'
    save_and_load_json({'k': 'v'}, path)
    content = path.read_text(encoding='utf-8')
    assert '\n' in content


def test_save_and_load_json_unicode_round_trip(tmp_path):
    path = tmp_path / 'data.json'
    result = save_and_load_json({'name': 'Иванов'}, path)
    assert result == {'name': 'Иванов'}


# Задание 7 -------------------------------------------------------------
def test_write_read_csv_round_trip(tmp_path):
    rows = [
        ['first_name', 'last_name', 'age'],
        ['ivan', 'ivanov', '27'],
        ['petr', 'petrov, jr', '37'],
    ]
    path = tmp_path / 'employees.csv'
    result = write_read_csv(rows, path)
    assert result == rows
    assert path.exists()


# Задание 8 -------------------------------------------------------------
@pytest.mark.parametrize('op,a,b,expected', [
    ('+', 7, 2, 9),
    ('-', 7, 2, 5),
    ('*', 7, 2, 14),
    ('/', 7, 2, 3.5),
    ('**', 2, 3, 8),
    ('-', 2, 7, -5),
    ('**', 2, -1, 0.5),
])
def test_calculate_operations(op, a, b, expected):
    assert calculate(op, a, b) == expected


def test_calculate_unknown_operation_raises():
    with pytest.raises(ValueError, match='%'):
        calculate('%', 1, 1)


def test_calculate_uses_dict_dispatch_not_elif():
    # Докстринг задания сам упоминает слово "elif" (объясняя, чего делать
    # не надо), поэтому проверяем только тело функции без docstring.
    source = inspect.getsource(calculate)
    func_node = ast.parse(source).body[0]
    body = func_node.body
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]  # пропускаем docstring
    code_only = '\n'.join(ast.get_source_segment(source, node) for node in body)
    assert 'elif' not in code_only, 'используйте словарь функций вместо цепочки elif'


# Задание 9 -------------------------------------------------------------
def test_moving_average_window_2():
    assert moving_average([1, 2, 3, 4, 5], 2) == [1.5, 2.5, 3.5, 4.5]


def test_moving_average_window_3():
    assert moving_average([1, 2, 3, 4, 5], 3) == pytest.approx([2.0, 3.0, 4.0])


def test_moving_average_window_too_large():
    assert moving_average([1, 2], 5) == []


def test_moving_average_window_equals_length():
    assert moving_average([1, 2, 3], 3) == pytest.approx([2.0])


def test_moving_average_window_1():
    assert moving_average([1, 2, 3], 1) == pytest.approx([1.0, 2.0, 3.0])


def test_moving_average_empty_values():
    assert moving_average([], 1) == []


# Задание 10 -------------------------------------------------------------
def test_first_n_odd_basic():
    assert first_n_odd([2, 4, 5, 6, 7, 8, 9, 10, 11], 3) == [5, 7, 9]


def test_first_n_odd_none_found():
    assert first_n_odd([2, 4, 6], 2) == []


def test_first_n_odd_exhausted_early():
    assert first_n_odd([1, 2, 3], 5) == [1, 3]


def test_first_n_odd_zero_requested():
    assert first_n_odd([1, 2, 3], 0) == []


def test_first_n_odd_is_lazy():
    # Задание явно просит останавливаться, найдя n чисел, а не строить
    # заранее список всех нечётных элементов. Проверяем это не по
    # исходному коду, а по поведению: генератор "взрывается", если из
    # него вытянуть больше элементов, чем нужно на самом деле –
    # реализация, которая сначала материализует весь iterable
    # (например, list(iterable) или списковое включение по всему
    # входу), должна упасть здесь вместо того, чтобы просто зависнуть.
    def guarded_numbers():
        count = 0
        while True:
            count += 1
            if count > 1000:
                raise AssertionError(
                    'first_n_odd прочитал слишком много элементов – '
                    'нужно останавливаться сразу после того, как найдено n нечётных'
                )
            yield count

    assert first_n_odd(guarded_numbers(), 3) == [1, 3, 5]
