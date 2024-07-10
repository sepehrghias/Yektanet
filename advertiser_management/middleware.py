class AddIPToRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the IP address from the request
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            # In case of multiple proxies, take the first one
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Add the IP address to the request object
        request.ip = ip

        # Call the next middleware or view
        response = self.get_response(request)
        return response
