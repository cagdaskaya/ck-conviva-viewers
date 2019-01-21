import datetime


def prettify_date(epoch):
    return datetime.datetime.fromtimestamp(epoch / 1000, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")


def prettify_time(epoch):
    td = str(datetime.timedelta(milliseconds=epoch)).split('.')[0]
    return f"{td.split(':')[0]}h {td.split(':')[1]}m {td.split(':')[2]}s"

