import json
from typing import Dict, List, Union


def group_by_departments(
        data: List[Dict[str, Union[str, int]]]
) -> Dict[str, List[Dict[str, Union[str, int]]]]:
    departments = {}
    for entry in data:
        dept = entry.get('department', 'Unknown')
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(entry)
    return departments


def payout_to_terminal(data: List[Dict[str, Union[str, int]]]) -> None:
    # Группировка по департаментам
    departments = group_by_departments(data)

    # Вывод результатов в терминал
    print(
        '                        name                         '
        'hours     rate     payout')
    for department, employees in departments.items():
        print(f'{department}')
        total_hours = 0
        total_payout = 0

        for emp in employees:
            name = emp.get('name', '').ljust(30)
            hours = str(emp.get('hours_worked', 0)).rjust(6)
            rate = str(emp.get('hourly_rate', 0)).rjust(6)
            payout = f'${emp.get("payout", 0)}'.rjust(10)
            print(
                f'-------------------- {name}{hours}    {rate}    {payout}')
            total_hours += emp.get('hours_worked', 0)
            total_payout += emp.get('payout', 0)

        hours_str = str(total_hours).rjust(6)
        payout_str = f'${total_payout}'.rjust(10)
        print(f'{"":51}{hours_str}               {payout_str}')

    return None


def payout_to_json(
        data: List[Dict[str, Union[str, int]]],
        output_file: str = 'output.json'
) -> None:
    # Группировка данных по департаментам для JSON
    departments = group_by_departments(data)

    # Формируем структурированный словарь для JSON
    result = {}
    for department, employees in departments.items():
        total_hours = sum(emp.get('hours_worked', 0) for emp in employees)
        total_payout = sum(emp.get('payout', 0) for emp in employees)
        result[department] = {
            'employees': [
                {
                    'name': emp.get('name', ''),
                    'hours_worked': emp.get('hours_worked', 0),
                    'hourly_rate': emp.get('hourly_rate', 0),
                    'payout': emp.get('payout', 0)
                }
                for emp in employees
            ],
            'total_hours': total_hours,
            'total_payout': total_payout
        }

    # Сохраняем в JSON-файл
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f'Данные успешно сохранены в файл "{output_file}"')
    except Exception as e:
        print(f'Ошибка при сохранении в файл "{output_file}": {e}')
