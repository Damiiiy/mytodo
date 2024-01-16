from django.urls import path, re_path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.dbd, name='home'),
    path('signup/', views.signup , name='signup'),
    path('login/', views.user_login , name='login'),
    path('logout/', views.user_logout , name='logout'),
    path('/home', views.dbd , name='login_home'),
    path('add_task/', views.add_task , name='create_task'),
    path('update_task/<int:task_id>/', views.update_task , name='update_tasks'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_tasks'),
    # re_path(r'^accounts/login/$', views.dbd, name='login_with_next'),  
    path('home/', views.dbd, name='home'),
    path('', views.dbd , name='dashboard'),
    path('test/', TemplateView.as_view(template_name='test.html') , name='test'),
]