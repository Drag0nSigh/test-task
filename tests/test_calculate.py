from calculate import payout


def test_payout_calculate():
    data = [
        {'hours_worked': 160, 'hourly_rate': 45},
        {'hours_worked': 150, 'hourly_rate': 35}
    ]
    expected = [
        {'hours_worked': 160, 'hourly_rate': 45, 'payout': 7200},
        {'hours_worked': 150, 'hourly_rate': 35, 'payout': 5250}
    ]
    result = payout(data)
    assert result == expected


def test_payout_missing_fields():
    data = [
        {'hours_worked': 160},
        {'hourly_rate': 35},
        {}
    ]
    expected = [
        {'hours_worked': 160, 'payout': 0},
        {'hourly_rate': 35, 'payout': 0},
        {'payout': 0}
    ]
    result = payout(data)
    assert result == expected


def test_payout_empty_list():
    data = []
    expected = []
    result = payout(data)
    assert result == expected
