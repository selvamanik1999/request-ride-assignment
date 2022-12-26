from collections import OrderedDict


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [OrderedDict(zip(columns, row)) for row in cursor.fetchall()]
