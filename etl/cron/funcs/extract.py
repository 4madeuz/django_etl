import psycopg2


def RowIterator(cursor, arraysize=1000):
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result


def modified(connection: psycopg2.connect, date, table):
    curs = connection.cursor()
    curs.execute(
        """
                SELECT id, updated_at
                FROM content.{}
                WHERE updated_at > '{}'
                ORDER BY updated_at
                LIMIT 100;
                """.format(
            table, date
        )
    )
    return curs


def person_filworks(connection: psycopg2.connect, objects, table):
    curs = connection.cursor()
    if len(objects) == 1:
        ids = f"('{objects[0].id.hex}')"
    else:
        ids = tuple(str(row.id) for row in objects)
    curs.execute(
        """
                SELECT fw.id, fw.updated_at
                FROM content.film_work fw
                LEFT JOIN content.{}_film_work pfw ON pfw.film_work_id = fw.id
                WHERE pfw.{}_id IN {}
                ORDER BY fw.updated_at
                """.format(
            table, table, ids
        )
    )
    return curs


def person_es(connection: psycopg2.connect, objects):
    curs = connection.cursor()
    if len(objects) == 1:
        ids = f"('{objects[0].id.hex}')"
    else:
        ids = tuple(str(row.id) for row in objects)
    curs.execute(
        """
    SELECT
    fw.id as id,
    fw.title,
    fw.description,
    fw.rating as imdb_rating,
    COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
        ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'),
       '[]'
        ) as actors,
    COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
        ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'),
       '[]'
        ) as writers,
    array_agg(DISTINCT g.name) as genre,
    string_agg(DISTINCT p.full_name, ', ') FILTER (WHERE pfw.role = 'actor') as actors_names,
    array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') as writers_names,
    string_agg(DISTINCT p.full_name, ', ') FILTER (WHERE pfw.role = 'director') as director
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE fw.id IN {}
    GROUP BY fw.id;
                """.format(
            ids
        )
    )
    return curs
