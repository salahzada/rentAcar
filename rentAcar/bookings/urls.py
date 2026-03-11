from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('',                        views.BookingListView.as_view(),    name='list'),
    path('<int:pk>/',               views.BookingDetailView.as_view(),  name='detail'),
    path('create/',                 views.BookingCreateView.as_view(),  name='create'),
    path('create/<int:car_id>/',    views.BookingCreateView.as_view(),  name='create_for_car'),
    path('<int:pk>/edit/',          views.BookingUpdateView.as_view(),  name='update'),
    path('<int:pk>/confirm/',       views.BookingConfirmView.as_view(), name='confirm'),
    path('<int:pk>/cancel/',        views.BookingCancelView.as_view(),  name='cancel'),
    path('<int:pk>/delete/',        views.BookingDeleteView.as_view(),  name='delete'),
]