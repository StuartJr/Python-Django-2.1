from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache


urlpatterns = [
	path('social/', include('social_django.urls', namespace = 'social')),
	path('captcha/', include('captcha.urls')),
	path('storys/',include('storys.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
	urlpatterns.append(path('static/<path:path>', never_cache(serve)))
	urlpatterns += static(settings.MEDIA_URL,
						 document_root = settings.MEDIA_ROOT)
