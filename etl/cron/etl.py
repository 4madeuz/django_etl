from contextlib import contextmanager

import backoff
import psycopg2
from dotenv import load_dotenv
from elasticsearch.helpers import BulkIndexError
from funcs import cron_settings, dсlasses, extract, load, states, transform
from psycopg2.errors import OperationalError
from psycopg2.extras import DictCursor

load_dotenv()


@contextmanager
def pg_context(dsl, cursor_fact):
    conn = psycopg2.connect(**dsl, cursor_factory=cursor_fact)
    yield conn
    conn.close()


@backoff.on_exception(backoff.expo, OperationalError)
def main():
    settings = cron_settings.Settings()
    dsl = {
        'dbname': settings.postgres_db,
        'user': settings.postgres_user,
        'password': settings.postgres_password,
        'host': settings.postgres_host,
        'port': settings.postgres_port,
    }
    print(dsl)
    keys = ['person', 'film_work', 'genre']
    with pg_context(dsl, cursor_fact=DictCursor) as pg_conn:
        state = states.State(states.JsonFileStorage('data.json'))
        for key in keys:
            date = state.get_state(key)
            curs = extract.modified(pg_conn, date, key)
            objects = transform.validate_pd(curs, dсlasses.UUidUpdated)
            if objects != []:
                last_state = objects[-1].updated_at
                if key != 'film_work':
                    filmwork_curs = extract.person_filworks(
                        pg_conn, objects, key
                    )
                    objects = transform.validate_pd(
                        filmwork_curs, dсlasses.UUidUpdated
                    )
                try:
                    person_to_es_curs = extract.person_es(pg_conn, objects)
                    person_to_es_objects = transform.update_es(
                        person_to_es_curs, dсlasses.EtlTransform
                    )
                    load.data(person_to_es_objects)
                    state.set_state(key, last_state.isoformat())
                except BulkIndexError:
                    person_to_es_curs = extract.person_es(pg_conn, objects)
                    person_to_es_objects = transform.create_es(
                        person_to_es_curs, dсlasses.EtlTransform
                    )
                    load.data(person_to_es_objects)
                    state.set_state(key, last_state.isoformat())


if __name__ == '__main__':
    main()
