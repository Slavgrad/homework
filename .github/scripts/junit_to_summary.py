"""
Превращает JUnit-XML отчёт pytest (--junitxml=results.xml) в
Markdown-таблицу для сводки запуска GitHub Actions (Job Summary).

Использование:
    python .github/scripts/junit_to_summary.py results.xml
"""

import sys
import xml.etree.ElementTree as ET


def load_cases(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return root.iter('testcase')


def case_status(case):
    if case.find('failure') is not None:
        return 'failure', case.find('failure')
    if case.find('error') is not None:
        return 'error', case.find('error')
    if case.find('skipped') is not None:
        return 'skipped', case.find('skipped')
    return 'passed', None


def short_reason(node):
    if node is None:
        return ''
    message = node.attrib.get('message', '') or (node.text or '')
    first_line = message.strip().splitlines()[0] if message.strip() else ''
    if len(first_line) > 120:
        first_line = first_line[:117] + '...'
    return first_line.replace('|', '\\|')


def main():
    if len(sys.argv) != 2:
        print('Usage: junit_to_summary.py <results.xml>', file=sys.stderr)
        return 1

    try:
        cases = list(load_cases(sys.argv[1]))
    except (ET.ParseError, FileNotFoundError):
        print('## Результаты проверки домашнего задания\n')
        print('Не удалось найти или разобрать отчёт тестов (results.xml).')
        return 0

    passed = sum(1 for c in cases if case_status(c)[0] == 'passed')
    total = len(cases)

    print('## Результаты проверки домашнего задания\n')
    print(f'**Пройдено тестов: {passed} / {total}**\n')

    if total == 0:
        print('Тесты не найдены.')
        return 0

    print('| Тест | Статус | Комментарий |')
    print('|---|---|---|')
    icons = {'passed': '✅', 'failure': '❌', 'error': '💥', 'skipped': '⏭️'}
    for case in cases:
        status, node = case_status(case)
        name = case.attrib.get('name', '?')
        print(f'| `{name}` | {icons[status]} {status} | {short_reason(node)} |')

    if passed < total:
        print('\nЧтобы увидеть подробности локально, запустите:\n')
        print('```bash\npytest tests/hw01 -v\n```')

    return 0


if __name__ == '__main__':
    sys.exit(main())
