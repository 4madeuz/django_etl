from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ['film_work']


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ['person']


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline,
    )

    # Отображение полей в списке
    list_display = (
        'title',
        'type',
        'created_at',
        'rating',
        'get_genres',
    )
    list_prefetch_related = ('genres',)

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'

    list_filter = ('type',)

    search_fields = ('title', 'description', 'id')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'description',
        'created_at',
    )

    search_fields = (
        'name',
        'description',
        'id',
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'created_at',
    )

    search_fields = (
        'full_name',
        'id',
    )
