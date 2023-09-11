from dataclasses import asdict


def RowIterator(cursor, arraysize=1000):
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result


def validate_pd(curs, dclass):
    objects = [dclass(**dict(row)) for row in RowIterator(curs)]
    return objects


def update_es(curs, dclass):
    raw_objects = [asdict(dclass(**dict(row))) for row in RowIterator(curs)]
    objects = []
    for obj in raw_objects:
        objects.append(
            {
                '_op_type': 'update',
                '_index': 'movies',
                '_id': obj['id'],
                'doc': {**obj},
            },
        )
    return objects


def create_es(curs, dclass):
    raw_objects = [asdict(dclass(**dict(row))) for row in RowIterator(curs)]
    objects = []
    for obj in raw_objects:
        objects.append({'_index': 'movies', '_id': obj['id'], **obj,},)
    return objects
