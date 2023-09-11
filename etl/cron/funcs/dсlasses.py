import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import model_validator
from pydantic.dataclasses import dataclass


@dataclass
class UUidMixin:
    id: UUID


@dataclass
class UUidUpdated(UUidMixin):
    updated_at: datetime.datetime

    @model_validator(mode='before')
    def pre_root(cls, values: Dict[str, Any]):
        if isinstance(values.kwargs['updated_at'], str):
            values.kwargs['updated_at'] = values.kwargs['updated_at'][:-3]
        else:
            values.kwargs['updated_at'] = values.kwargs['updated_at'].replace(
                tzinfo=None
            )
        return values


@dataclass
class TimeStampedMixin:
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @model_validator(mode='before')
    def pre_root(cls, values: Dict[str, Any]):
        if isinstance(values.kwargs['created_at'], str):
            values.kwargs['created_at'] = values.kwargs['created_at'][:-3]
            values.kwargs['updated_at'] = values.kwargs['updated_at'][:-3]
        else:
            values.kwargs['created_at'] = values.kwargs['created_at'].replace(
                tzinfo=None
            )
            values.kwargs['updated_at'] = values.kwargs['updated_at'].replace(
                tzinfo=None
            )
        return values


@dataclass
class FilmWork(UUidMixin, TimeStampedMixin):
    id: UUID
    title: str
    description: Optional[str]
    creation_date: Optional[str]
    file_path: Optional[str]
    rating: Optional[float]
    type = Optional[str]

    def name_yourself():
        return 'film_work'


@dataclass
class Person(UUidMixin, TimeStampedMixin):
    full_name: Optional[str]

    def name_yourself():
        return 'person'


@dataclass
class Genre(UUidMixin, TimeStampedMixin):
    name: str
    description: Optional[str]

    def name_yourself():
        return 'genre'


@dataclass
class GenreFilmwork(UUidMixin):
    film_work_id: UUID
    genre_id: UUID
    created_at: datetime.datetime

    @model_validator(mode='before')
    def pre_root(cls, values: Dict[str, Any]):
        if isinstance(values.kwargs['created_at'], str):
            values.kwargs['created_at'] = values.kwargs['created_at'][:-3]
        else:
            values.kwargs['created_at'] = values.kwargs['created_at'].replace(
                tzinfo=None
            )
        return values

    def name_yourself():
        return 'genre_film_work'


@dataclass
class PersonFilmwork(UUidMixin):
    person_id: UUID
    film_work_id: UUID
    role: Optional[str]
    created_at: datetime.datetime

    @model_validator(mode='before')
    def pre_root(cls, values: Dict[str, Any]):
        if isinstance(values.kwargs['created_at'], str):
            values.kwargs['created_at'] = values.kwargs['created_at'][:-3]
        else:
            values.kwargs['created_at'] = values.kwargs['created_at'].replace(
                tzinfo=None
            )
        return values

    def name_yourself():
        return 'person_film_work'


@dataclass
class EtlTransform:
    id: UUID
    title: str
    description: Optional[str]
    imdb_rating: Optional[float]
    actors: Optional[list]
    writers: Optional[list]
    genre: list
    actors_names: Optional[str]
    writers_names: Optional[list]
    director: Optional[str]

    @model_validator(mode='before')
    def pre_root(cls, values: Dict[str, Any]):
        if values.kwargs['director'] is None:
            values.kwargs['director'] = ''
        return values
