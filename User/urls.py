from django.urls import path
from .views import UserLogoutView ,UserLoginView,SignupUserView
from . import views
from django.contrib.auth import views as auth_views

app_name = "user"

urlpatterns = [
   path('login/', UserLoginView.as_view(), name='login'),
   path("logout/",UserLogoutView.as_view(), name="logout"),
   path('signup/', SignupUserView.as_view(),  name='signup'),
   path('contact/<int:pk>', views.contact,  name='contact'),
   path('notifications/<int:pk>', views.show_notifications, name='show_notifications'),
   path('notifications/detail/<int:pk>/<int:notification_id>', views.view_notification, name='detail_notifications'),

]