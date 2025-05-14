import pytest
from unittest.mock import patch, mock_open
from export import group_by_departments, payout_to_terminal, payout_to_json


@pytest.fixture
def sample_data():
    return [
        {
            "department": "HR",
            "name": "Grace Lee",
            "hours_worked": 160,
            "hourly_rate": 45,
            "payout": 7200
        },
        {
            "department": "Marketing",
            "name": "Henry Martin",
            "hours_worked": 150,
            "hourly_rate": 35,
            "payout": 5250
        },
        {
            "name": "Karen White",
            "hours_worked": 165,
            "hourly_rate": 50,
            "payout": 8250}
    ]


def test_group_by_departments(sample_data):
    expected = {
        "HR": [
            {
                "department": "HR",
                "name": "Grace Lee",
                "hours_worked": 160,
                "hourly_rate": 45,
                "payout": 7200
            }
        ],
        "Marketing": [
            {
                "department": "Marketing",
                "name": "Henry Martin",
                "hours_worked": 150,
                "hourly_rate": 35,
                "payout": 5250
            }
        ],
        "Unknown": [
            {
                "name": "Karen White",
                "hours_worked": 165,
                "hourly_rate": 50,
                "payout": 8250}
        ]
    }
    result = group_by_departments(sample_data)
    assert result == expected


def test_group_by_departments_empty():
    data = []
    expected = {}
    result = group_by_departments(data)
    assert result == expected


@patch('builtins.print')
def test_payout_to_terminal(mock_print, sample_data):
    payout_to_terminal(sample_data)
    expected_calls = [
        '                        name                         hours     rate  '
        '   payout',
        'HR',
        '-------------------- Grace Lee                        160        45  '
        '      $7200',
        '                                                      160            '
        '       $7200',
        'Marketing',
        '-------------------- Henry Martin                     150        35  '
        '      $5250',
        '                                                      150            '
        '       $5250',
        'Unknown',
        '-------------------- Karen White                      165        50  '
        '      $8250',
        '                                                      165            '
        '       $8250'
    ]
    calls = [call[0][0] for call in mock_print.call_args_list]
    assert calls == expected_calls


@patch('builtins.open', new_callable=mock_open)
@patch('builtins.print')
def test_payout_to_json(mock_print, mock_file, sample_data):
    payout_to_json(sample_data, 'test.json')
    expected_json = {
        'HR': {
            'employees': [
                {
                    'name': 'Grace Lee',
                    'hours_worked': 160,
                    'hourly_rate': 45,
                    'payout': 7200
                }
            ],
            'total_hours': 160,
            'total_payout': 7200
        },
        'Marketing': {
            'employees': [
                {
                    'name': 'Henry Martin',
                    'hours_worked': 150,
                    'hourly_rate': 35,
                    'payout': 5250
                }
            ],
            'total_hours': 150,
            'total_payout': 5250
        },
        'Unknown': {
            'employees': [
                {
                    'name': 'Karen White',
                    'hours_worked': 165,
                    'hourly_rate': 50,
                    'payout': 8250
                }
            ],
            'total_hours': 165,
            'total_payout': 8250
        }
    }

    written_data = ''.join(
        call[0][0] for call in mock_file().write.call_args_list)
    import json
    written_json = json.loads(written_data)
    assert written_json == expected_json
    mock_print.assert_called_with('Данные успешно сохранены в файл '
                                  '"test.json"')


@patch('builtins.open', side_effect=IOError('Ошибка записи'))
@patch('builtins.print')
def test_payout_to_json_io_error(mock_print, mock_file, sample_data):
    payout_to_json(sample_data, 'test.json')
    mock_print.assert_called_with(
        'Ошибка при сохранении в файл "test.json": Ошибка записи'
    )
