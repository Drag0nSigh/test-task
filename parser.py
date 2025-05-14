from typing import Dict, List, Union


def parse_csv(csv_text: str) -> List[Dict[str, Union[str, int]]]:
    lines = csv_text.strip().split('\n')
    headers = lines[0].split(',')

    # Нормализуем название поля для почасовой ставки
    for i, header in enumerate(headers):
        if header in ['hourly_rate', 'rate', 'salary']:
            headers[i] = 'hourly_rate'
        elif header in ['id', 'emp_id', 'employee_id']:
            headers[i] = 'id'
        elif header in ['department', 'dept', 'division']:
            headers[i] = 'department'
        elif header in [
            'hours_worked', 'hours', 'worked_hours', 'hoursworked'
        ]:
            headers[i] = 'hours_worked'
        elif header in ['name', 'fullname', 'full_name']:
            headers[i] = 'name'
        elif header in ['email', 'e-mail', 'e_mail']:
            headers[i] = 'email'

    data = []

    # Обрабатываем строки с данными (пропускаем заголовок)
    for line in lines[1:]:
        values = line.split(',')

        row = {}
        for i, header in enumerate(headers):
            # Преобразуем числовые поля в int, остальные оставляем строками
            if header in ['id', 'hours_worked', 'hourly_rate']:
                row[header] = int(values[i])
            else:
                row[header] = values[i]

        # Добавляем словарь в список
        data.append(row)

    return data
