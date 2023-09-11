import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'),)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        Movie = _('movie')
        TW_show = _('tw_show')

    title = models.TextField(_('title'))
    description = models.TextField(_('description'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
    )
    type = models.TextField(
        _('type'), choices=Type.choices, default=Type.Movie, null=True
    )
    file_path = models.FilePathField(
        _('file'), blank=True, null=True, path='movies/'
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')
    creation_date = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'
        indexes = [models.Index(fields=['rating'])]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'genre'], name='unique_film_work_genre'
            )
        ]


class PersonFilmwork(UUIDMixin):
    class Role(models.TextChoices):
        Actor = _('actor')
        Director = _('director')
        Writer = _('writer')

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    role = models.TextField(
        _('role'), choices=Role.choices, default=Role.Actor, blank=True
    )

    class Meta:
        db_table = 'content"."person_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'],
                name='unique_film_work_pseron_role',
            )
        ]
