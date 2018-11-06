import datetime


def format_date(date_, format_='%Y-%m-%d'):
    if date_:
        return datetime.date.strftime(date_, format_)
    return None


def format_datetime(datetime_):
    if datetime_:
        return datetime_.strftime('%Y-%m-%d %H:%M:%S')
    return None


def fecha_actual(format_='%Y-%m-%d') -> str:
    return datetime.date.strftime(datetime.date.today(), format_)
