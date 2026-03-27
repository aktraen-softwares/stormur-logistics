class CustomHeadersMiddleware:
    """Inject custom response headers to mimic production stack."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Powered-By"] = "Django"
        response["Server"] = "nginx/1.22.1"
        return response
