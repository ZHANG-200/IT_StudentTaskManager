from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('courses/', views.view_courses_page, name='view_courses_page'),
    path('course/add/', views.add_course, name='add_course'),
    path('course/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('course/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.view_courses, name='view_courses'),
    path('assignment/add/', views.add_assignment, name='add_assignment'),
    path('assignment/<int:assignment_id>/done/', views.mark_assignment_done, name='mark_assignment_done'),
    path('assignment/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('assignment/edit/<int:assignment_id>/', views.edit_assignment, name='edit_assignment'),
    path('assignment/filter/', views.filter_assignment, name='filter_assignment'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('', views.view_courses, name='home'),  
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
]