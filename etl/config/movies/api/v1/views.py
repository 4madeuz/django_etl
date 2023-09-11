from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, UUIDField
from django.db.models.functions import Lower
from django.http import HttpResponse, JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork, PersonFilmwork

UUIDField.register_lookup(Lower)


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        return (
            Filmwork.objects.all()
            .prefetch_related('genres', 'persons')
            .values(
                'id', 'title', 'description', 'creation_date', 'rating', 'type'
            )
            .annotate(genres=ArrayAgg('genres__name', distinct=True))
            .annotate(
                actors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=PersonFilmwork.Role.Actor),
                    distinct=True,
                )
            )
            .annotate(
                directors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=PersonFilmwork.Role.Director),
                    distinct=True,
                )
            )
            .annotate(
                writers=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=PersonFilmwork.Role.Writer),
                    distinct=True,
                )
            )
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )
        if page.has_next():
            next = page.next_page_number()
        else:
            next = None
        if page.has_previous():
            previous = page.previous_page_number()
        else:
            previous = None
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'next': next,
            'prev': previous,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = {
            'results': list(self.get_queryset().filter(id=self.kwargs['id'])),
        }
        return context


def api(request):
    return HttpResponse('My best API')
