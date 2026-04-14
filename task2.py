from datetime import datetime

users = [
    {"name": "Bill Gates", "birthday": datetime(1955, 10, 28).date()},
    {"name": "Friday", "birthday": datetime(1988, 7, 4).date()},
    {"name": "Monday", "birthday": datetime(1985, 4, 18).date()},
]

def get_birthdays_per_week(users):
    today = datetime.today().date()
    result = {}

    for user in users:
        name = user["name"]
        birthday = user["birthday"]

        birthday_this_year = birthday.replace(year=today.year)

        delta_days = (birthday_this_year - today).days

        if 0 <= delta_days < 7:
            weekday = birthday_this_year.weekday()

            if weekday >= 5:
                day_name = "Monday"
            else:
                day_name = birthday_this_year.strftime("%A")

            if day_name not in result:
                result[day_name] = []

            result[day_name].append(name)

    return result

print(get_birthdays_per_week(users))