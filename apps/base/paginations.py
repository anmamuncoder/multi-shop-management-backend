from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response

class BasePagination(PageNumberPagination):
    page_size = 10                  # items per page
    page_size_query_param = "size"   
    max_page_size = 10

    def get_page_size(self, request):
        if request.query_params.get("size"):
            return super().get_page_size(request)

        page = request.query_params.get(self.page_query_param, 1)
        return 20 if str(page) == "1" else 20

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "data": data  # <-- changed from "results" to "data"
        })
     
     
class BaseCursorPagination(CursorPagination):
    page_size = 100
    ordering = "-created_at"   #  must have ordering

    def get_paginated_response(self, data):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "data": data
        })
