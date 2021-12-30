from datetime import datetime
from jsonschema import FormatChecker

format_checker = FormatChecker()

@format_checker.checks("date", ValueError)
def strict_date_check(value):
    if value is None:
        return False

    datetime.strptime(value, "%Y-%m-%d")
    return True
