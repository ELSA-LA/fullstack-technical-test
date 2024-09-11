from django.utils.deprecation import MiddlewareMixin


class JWTAuthCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Obtener el token de las cookies
        access_token = request.COOKIES.get("access_token")

        if access_token:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
