from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class BasePagination(PageNumberPagination):
    page_size = 10                  # items per page
    page_size_query_param = "size"   
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "data": data  # <-- changed from "results" to "data"
        })