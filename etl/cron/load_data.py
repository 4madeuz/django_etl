import sqlite3

from dotenv import load_dotenv
from funcs import cron_settings
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite_to_postgres import dсlasses, pg, sqlite

load_dotenv()

datclasses = [
    dсlasses.FilmWork,
    dсlasses.Person,
    dсlasses.Genre,
    dсlasses.GenreFilmwork,
    dсlasses.PersonFilmwork,
]


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    for dclass in datclasses:
        objects = sqlite.sqlite_extract(connection, dclass)
        pg.save_data(pg_conn, objects, dclass)


if __name__ == '__main__':
    settings = cron_settings.Settings()
    dsl = {
        'dbname': settings.postgres_db,
        'user': settings.postgres_user,
        'password': settings.postgres_password,
        'host': settings.postgres_host,
        'port': settings.postgres_port,
    }
    print(dsl)
    with sqlite.conn_context(
        'sqlite_to_postgres/db.sqlite'
    ) as sqlite_conn, pg.pg_context(dsl, cursor_fact=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
