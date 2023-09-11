import sqlite3
from contextlib import contextmanager
from dataclasses import asdict, astuple


def RowIterator(cursor, arraysize=1000):
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def sqlite_extract(connection: sqlite3.Connection, dclass):
    curs = connection.cursor()
    curs.execute(f'Select * FROM {dclass.name_yourself()}')
    objects = [astuple(dclass(**dict(row))) for row in RowIterator(curs)]
    return objects
