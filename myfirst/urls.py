from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('storys/',include('storys.urls')),
    path('admin/', admin.site.urls),
]
