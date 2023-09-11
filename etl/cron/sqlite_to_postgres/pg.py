from contextlib import contextmanager
from dataclasses import astuple, fields

import psycopg2
from psycopg2.extras import register_uuid


@contextmanager
def pg_context(dsl, cursor_fact):
    conn = psycopg2.connect(**dsl, cursor_factory=cursor_fact)
    yield conn
    conn.close()


def save_data(connection: psycopg2.connect, objects, dclass):
    curs = connection.cursor()
    column_names = [field.name for field in fields(dclass)]
    register_uuid()
    col_count = ', '.join(['%s'] * len(column_names))
    bind_values = ','.join(
        curs.mogrify(f'({col_count})', row).decode('utf-8') for row in objects
    )
    q = (
        f'INSERT INTO content.{dclass.name_yourself()} ('
        f'{",".join(column_names)}) VALUES {bind_values} '
        f' ON CONFLICT (id) DO NOTHING;'
    )
    curs.execute(q)
    connection.commit()


def extract_data(connection: psycopg2.connect, dclass):
    curs = connection.cursor()
    curs.execute(f'Select * FROM content.{dclass.name_yourself()}')
    objects = [astuple(dclass(**dict(row))) for row in curs.fetchall()]
    return objects
