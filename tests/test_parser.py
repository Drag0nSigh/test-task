from parser import parse_csv


def test_parse_csv_single_row():
    csv_text = ('department,id,email,name,hours_worked,rate\n'
                'HR,101,grace@example.com,Grace Lee,160,45')
    expected = [
        {
            'department': 'HR',
            'id': 101,
            'email': 'grace@example.com',
            'name': 'Grace Lee',
            'hours_worked': 160,
            'hourly_rate': 45
        }
    ]
    result = parse_csv(csv_text)
    assert result == expected


def test_parse_csv_multiple_rows():
    csv_text = ('department,id,email,name,hours_worked,rate\n'
                'HR,101,grace@example.com,Grace Lee,160,45\n'
                'Marketing,102,henry@example.com,Henry Martin,150,35')
    expected = [
        {
            'department': 'HR',
            'id': 101,
            'email': 'grace@example.com',
            'name': 'Grace Lee',
            'hours_worked': 160,
            'hourly_rate': 45
        },
        {
            'department': 'Marketing',
            'id': 102,
            'email': 'henry@example.com',
            'name': 'Henry Martin',
            'hours_worked': 150,
            'hourly_rate': 35
        }
    ]
    result = parse_csv(csv_text)
    assert result == expected


def test_parse_csv_normalize_salary():
    csv_text = ('email,name,department,hours_worked,salary,id\n'
                'karen@example.com,Karen White,Sales,165,50,201')
    expected = [
        {
            'email': 'karen@example.com',
            'name': 'Karen White',
            'department': 'Sales',
            'hours_worked': 165,
            'hourly_rate': 50,
            'id': 201
        }
    ]
    result = parse_csv(csv_text)
    assert result == expected


def test_parse_csv_empty_input():
    csv_text = 'department,id,email,name,hours_worked,rate\n'
    expected = []
    result = parse_csv(csv_text)
    assert result == expected
