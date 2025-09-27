class ForceHttpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Force HTTP for all requests
        if 'HTTP_X_FORWARDED_PROTO' in request.META:
            if request.META['HTTP_X_FORWARDED_PROTO'] == 'https':
                request.META['HTTP_X_FORWARDED_PROTO'] = 'http'
        return self.get_response(request)
