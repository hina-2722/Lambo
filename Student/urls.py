from django.urls import path
from .views import Mypage,Children
from . import views

app_name = "student"

urlpatterns = [
    path('mypage/<int:pk>', Mypage.as_view(), name='mypage'),
    path('list', Children.as_view(), name='children'),
    path('checkin/<int:pk>', views.checkin, name='checkin'),
    path('checkout/<int:pk>', views.checkout, name='checkout'),
    path('history/<int:pk>', views.attendance_history, name='history'),
    path('tuition/<int:pk>/', views.tuition_list, name='tuition_list'),
    path('<int:pk>/reservation', views.student_reservation, name='reservation'),
    path('report/<int:pk>', views.report, name='report'),
    path('report/detail/<int:pk>/<int:report_id>', views.report_detail, name='report_detail'),
    path('benefit<int:pk>/', views.benefit, name='benefit'),
    path('ticket_purchase/<int:pk>', views.TicketPurchaseView, name='ticket_purchase'),
    path('workbook/<int:pk>', views.workbook_list, name='workbook'),
    path('questionnaire/<int:pk>', views.teacher_evaluation_form, name='questionnaire'),

    path('receipt/<int:pk>/', views.generate_receipt_pdf, name='receipt'),
  
]