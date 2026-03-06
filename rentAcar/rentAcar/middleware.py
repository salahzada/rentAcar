import time
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.middleware.csrf import get_token

IDLE_TIMEOUT = 60 * 5  # 5 minutes

class IdleSessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = time.time()

            if last_activity and (now - last_activity) > IDLE_TIMEOUT:
                logout(request)
                return redirect(f'/accounts/login/?next={request.path}')

            request.session['last_activity'] = now

        # Force refresh CSRF token on every request
        get_token(request)

        return self.get_response(request)