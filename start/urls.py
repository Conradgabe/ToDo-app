from django.urls import path
from . import views

app_name = 'start'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='LoginView'),
]