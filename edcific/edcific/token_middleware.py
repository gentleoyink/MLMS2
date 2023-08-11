class TokenAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract the token from the cookie
        token = request.COOKIES.get('auth_token')

        print("Token from cookie:", token)

        # If the token is present in the cookie, set it in the Authorization header
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
            print("Authorization header set:", request.META['HTTP_AUTHORIZATION'])


        response = self.get_response(request)
        return response
