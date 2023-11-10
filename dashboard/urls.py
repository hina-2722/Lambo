from django.urls import path
from . import views


app_name = "dashboard"
urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create_student/', views.student_create, name='student_create'),
    path('<int:pk>/', views.student_detail, name='student_detail'),

    path('tuition-list/', views.tuition_list, name='tuition_list'),
    path('E_tuition-list/', views.E_tuition_list, name='E_tuition_list'),

    path('sales/', views.caluculate, name='caluculate'),

    path('project_list/', views.project_list, name='project_list'),
    path('project_edit<int:pk>/', views.project_edit, name='project_edit'),
    path('create_instructor/', views.instructor_create, name='add_instructor'),

    path('reservations_list/', views.reservation_list_view, name='reservation_list'),
    path('reservations/today', views.todays_lesson_view, name='todays_lesson'),
    path('instructor_list/', views.instructor_list, name='instructor_list'),
    path('instructor/<int:pk>/', views.instructor_detail, name='instructor_detail'),

    path('contact_list/', views.contact_list, name='contact_list'),
    path('contact_detail/<int:pk>', views.contact_detail, name='contact_detail'),

    path('create_notifications/', views.create_notifications, name='create_notifications'),

    path('questionnaire_answer/', views.questionnaire_answer, name='questionnaire_answer'),
    path('workbook/', views.add_workbook, name='workbook'),

]