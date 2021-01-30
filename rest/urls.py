from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.user.urls')),
    path('api/', include('app.twitter.urls')),
]
