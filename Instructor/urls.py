from django.urls import path
from .views import index,Todaysclass
from . import views

app_name = 'instructor'

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('todaysclass/<int:pk>', Todaysclass.as_view(), name='todays_class'),
    path('historyclass/<int:pk>', views.History_class, name='history_class'),
    path('available/<int:pk>', views.create_available, name='available'),
    path('sarary/<int:pk>', views.sarary, name='sarary'),
]