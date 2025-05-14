from unittest.mock import patch, MagicMock
from main import parse_arguments, process_files, main


# Тест парсинга аргументов
@patch('sys.argv', ['main.py', 'data1.csv', 'data2.csv', '--report', 'payout'])
def test_parse_arguments():
    args = parse_arguments()
    assert args.files == ['data1.csv', 'data2.csv']
    assert args.report == 'payout'
    assert args.output == 'output'


# Тест process_files
@patch('sys.exit')
@patch('builtins.print')
@patch('builtins.open', new_callable=MagicMock)
def test_process_files(mock_open, mock_print, mock_exit):
    file_mock = MagicMock()
    file_mock.read.return_value = (
        'department,id,email,name,hours_worked,rate\n'
        'HR,101,grace@example.com,Grace Lee,160,45'
    )
    mock_open.return_value.__enter__.return_value = file_mock

    file_paths = ['data1.csv']
    expected = [
        {
            'department': 'HR', 'id': 101,
            'email': 'grace@example.com',
            'name': 'Grace Lee',
            'hours_worked': 160,
            'hourly_rate': 45
        }
    ]
    result = process_files(file_paths)
    assert result == expected


@patch('sys.exit')
@patch('builtins.open', side_effect=IOError('Файл не найден'))
@patch('builtins.print')
def test_process_files_file_not_found(mock_print, mock_open, mock_exit):
    file_paths = ['data1.csv']
    result = process_files(file_paths)
    assert result == []
    mock_print.assert_any_call('Ошибка: ни один файл не был успешно '
                               'обработан.')
    mock_exit.assert_called_with(1)


@patch('builtins.open', new_callable=MagicMock)
@patch('builtins.print')
@patch('sys.exit')
def test_process_files_no_success(mock_exit, mock_print, mock_open):
    mock_open.return_value.read.return_value = 'invalid_data'
    file_paths = ['data1.csv']
    process_files(file_paths)
    mock_print.assert_called_with('Ошибка: ни один файл не был успешно '
                                  'обработан.')
    mock_exit.assert_called_with(1)


@patch('main.parse_arguments')
@patch('main.process_files')
@patch('main.payout')
@patch('main.payout_to_terminal')
@patch('main.payout_to_json')
@patch('sys.exit')
def test_main_payout_report(
        mock_exit,
        mock_payout_to_json,
        mock_payout_to_terminal,
        mock_payout,
        mock_process_files,
        mock_parse_args
):
    mock_parse_args.return_value = MagicMock(
        files=['data1.csv'], report='payout', output='result'
    )
    mock_process_files.return_value = [
        {
            'department': 'HR',
            'hours_worked': 160,
            'hourly_rate': 45
        }
    ]
    mock_payout.return_value = [
        {
            'department': 'HR',
            'hours_worked': 160,
            'hourly_rate': 45,
            'payout': 7200
        }
    ]

    main()

    mock_process_files.assert_called_with(['data1.csv'])
    mock_payout.assert_called_once()
    mock_payout_to_terminal.assert_called_once()
    mock_payout_to_json.assert_called_with(
        mock_payout.return_value, output_file='result.json'
    )
    mock_exit.assert_called_with()
