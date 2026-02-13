from django.contrib import admin
from django.urls import path
from user_portal import views as user_views
from staff_portal import views as staff_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # User / Student Routes 
    path('', user_views.index, name='index'),
    path('register/', user_views.register_student, name='student_register'),
    path('login/', user_views.login_student, name='student_login'),
    path('logout/', user_views.logout_student, name='student_logout'),
    path('dashboard/', user_views.student_dashboard, name='student_dashboard'),

    path('assessment/<int:assessment_id>/take/', user_views.take_assessment, name='take_assessment'),
    path('assessment/<int:assessment_id>/submit/', user_views.submit_assessment, name='submit_assessment'),
    path('assessment/<int:assessment_id>/results/', user_views.view_results, name='view_results'),

    # Staff / Admin Routes
    path('staff/login/', staff_views.admin_login, name='admin_login'),
    path('staff/dashboard/', staff_views.admin_dashboard, name='admin_dashboard'),
    path('staff/create/', staff_views.create_assessment, name='create_assessment'),
    path('staff/assessment/<int:assessment_id>/add-question/', staff_views.add_question, name='add_question'),
    path('staff/assessment/<int:assessment_id>/delete/', staff_views.delete_assessment, name='delete_assessment'),
]