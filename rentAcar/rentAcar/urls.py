from django.contrib import admin
from django.urls import path, include
from profiles.views import CustomLoginView, RegisterView,HomeView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('bookings/', include('bookings.urls')),
    path('cars/', include('cars.urls')),
]