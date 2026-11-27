from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add-application/', views.add_application, name='add_application'),
    path('my-applications/', views.application_list, name='application_list'),
    path('edit-application/<int:id>/', views.edit_application, name='edit_application'),
    path('delete-application/<int:id>/', views.delete_application, name='delete_application'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upcoming-interviews/', views.upcoming_interviews, name='upcoming_interviews'),

]