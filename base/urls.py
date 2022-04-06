from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'base'

urlpatterns = [
    path('', views.Tasklist.as_view(), name='Tasklist'),
    path('details/<int:pk>', views.TaskDetail.as_view(), name='TaskDetail'),
    path('create-task/', views.TaskCreate.as_view(), name='TaskCreate'),
    path('update-task/<int:pk>', views.TaskUpdate.as_view(), name='TaskUpdate'),
    path('delete-task/<int:pk>', views.TaskDelete.as_view(), name='TaskDelete'),
    path('login/', views.CustomLoginView.as_view(), name='LoginView'),
    path('logout/', LogoutView.as_view(next_page='base:LoginView'), name='LogoutView'),
    path('register/', views.RegisterPage.as_view(), name='Register')
]