import argparse
import sys
from typing import List, Dict, Union

from calculate import payout
from parser import parse_csv
from export import payout_to_json, payout_to_terminal


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Обработка файлов и создание отчётов.'
    )
    parser.add_argument(
        'files',
        nargs='+',
        help='Пути к файлам для обработки (например, data1.csv data2.csv)'
    )
    parser.add_argument(
        '--report',
        required=True,
        choices=['payout'],  # В будущем можно добавить другие типы отчётов
        help='Тип отчёта: "payout" для отчёта по выплатам'
    )
    parser.add_argument(
        '--output',
        default='output',
        help='Имя выходного файла для отчёта (по умолчанию: output)'
    )
    return parser.parse_args()


def process_files(file_paths: List[str]) -> List[Dict[str, Union[str, int]]]:
    combined_result = []

    for file_path in file_paths:
        # Читаем содержимое файла
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_text = file.read()
        except Exception as e:
            print(f'Ошибка при чтении файла "{file_path}": {e}')
            continue

        # Парсим CSV с помощью функции parse_csv
        try:
            result = parse_csv(csv_text)
            combined_result.extend(result)
        except Exception as e:
            print(f'Ошибка при парсинге файла "{file_path}": {e}')
            continue

    if not combined_result:
        print('Ошибка: ни один файл не был успешно обработан.')
        sys.exit(1)

    return combined_result


def main():
    # Парсим аргументы командной строки
    args = parse_arguments()

    # Обрабатываем файлы
    combined_result = process_files(args.files)

    # Выбираем тип отчёта
    if args.report == 'payout':
        # Добавляем payout для вывода
        combined_result = payout(combined_result)
        payout_to_terminal(combined_result)
        payout_to_json(combined_result, output_file=f'{args.output}.json')

    sys.exit()


if __name__ == '__main__':
    main()
