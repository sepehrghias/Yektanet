from django.core.exceptions import PermissionDenied

class FilterIPMiddleware(object):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        request.ip = ip