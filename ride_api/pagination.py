from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from ride_api.serializers import RequesterSerializer


class RequesterPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        results = RequesterSerializer(data, context={'request': self.request}, many=True).data
        page_size = int(self.request.query_params.get(self.page_size_query_param, self.page_size))
        return Response({
            'total': self.page.paginator.count,
            'page': int(self.request.query_params.get('page', 1)),
            'page_size': min(len(results), page_size),
            'results': results
        }, status=status.HTTP_200_OK)
