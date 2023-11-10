from django.urls import path
from .views import create_reservation,confirm_reservation,schedule_calendar,schedule_detail,create_report

app_name = 'reservation'

urlpatterns = [
    path('create/<int:pk>', create_reservation, name='create_reservation'),
    path('schedule/<int:pk>', schedule_calendar, name='schedule_list'),
    path('schedule/<int:year>/<int:month>/<int:day>/<int:pk>/', schedule_detail, name='available_instructor'),
    path('confirm/<int:pk>/',confirm_reservation, name='confirm'),

    path('report_create/<int:pk>/<int:reservation_pk>',create_report, name='report_create'),
]