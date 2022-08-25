import datetime


def prettify_date(epoch):
    return datetime.datetime.fromtimestamp(epoch / 1000, datetime.timezone.utc).strftime("%d-%m-%Y %H:%M:%S %Z")


def prettify_time(epoch):
    td = str(datetime.timedelta(milliseconds=epoch)).split('.')[0]
    return f"{td.split(':')[0]}h {td.split(':')[1]}m {td.split(':')[2]}s"


def v_lister(lod, target):
    return [d[target] for d in lod]


def v_setter(lod, target):
    return {d[target] for d in lod}


def v_adder(lod, target):
    return sum([d[target] for d in lod])


def calc_percentages(lod, target):
    fl = v_lister(lod, target)
    fs = v_setter(lod, target)
    return [(round((100 * fl.count(i) / len(fl))), i) for i in fs]

