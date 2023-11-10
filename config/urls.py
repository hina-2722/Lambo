from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Student.urls")),
    path('user/', include("User.urls")),
    path('dashboard/', include('dashboard.urls')),
    path('instructor/', include('Instructor.urls')),
    path('reservation/', include('Reservation.urls')),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)