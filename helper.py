import datetime

def prettify_date(epoch):
    return datetime.datetime.fromtimestamp(epoch / 1000, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
