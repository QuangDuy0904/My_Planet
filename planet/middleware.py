from django.contrib.auth import logout

class AutoLogoutOnReloadMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Nếu truy cập trang chủ hoặc bất kỳ trang nào và đã login -> tự logout
        if request.user.is_authenticated and request.path in ['/', '/login/', '/register/']:
            logout(request)
        response = self.get_response(request)
        return response