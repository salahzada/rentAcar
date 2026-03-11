from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('',                  views.CarListView.as_view(),   name='list'),
    path('<int:pk>/',         views.CarDetailView.as_view(), name='detail'),
    path('create/',           views.CarCreateView.as_view(), name='create'),
    path('<int:pk>/edit/',    views.CarUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/',  views.CarDeleteView.as_view(), name='delete'),
]