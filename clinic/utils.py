from rest_framework.pagination import PageNumberPagination


def datetime_to_string(datetime):
    """
    Take a datetime object and return a nicely formatted string, eg: Aug 06, 2020 at 07:21 PM. 
    """
    return datetime.strftime("%b %d, %Y at %I:%M %p")


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom page number pagination.
    """
    page_query_param = 'page'
    page_size = 3
    page_size_query_param = 'size'  # items per page
    max_page_size = 10