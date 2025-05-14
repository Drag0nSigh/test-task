from typing import Dict, List, Union


def payout(
        data: List[Dict[str, Union[str, int]]]
) -> List[Dict[str, Union[str, int]]]:
    for man in data:
        man['payout'] = man.get('hours_worked', 0) * man.get('hourly_rate', 0)

    return data
