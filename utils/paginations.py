from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'pages_count': len(self.page.paginator.page_range),
            'results': data
        })

    def paginate_queryset(self, queryset, request, view=None):
        page = request.query_params.get('page')
        if page is None:
            self.page_size = queryset.count()

        return super(CustomPagination, self).paginate_queryset(queryset, request, view=None)


class ProfilePagination(PageNumberPagination):
    page_size = 24

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'pages_count': len(self.page.paginator.page_range),
            'results': data
        })

    def paginate_queryset(self, queryset, request, view=None):
        page = request.query_params.get('page')
        if page is None:
            self.page_size = queryset.count()

        return super(ProfilePagination, self).paginate_queryset(queryset, request, view=None)
