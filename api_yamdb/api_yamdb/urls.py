
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('static/redoc.yaml', serve, {
        'document_root': settings.STATICFILES_DIRS[0], 'path': 'redoc.yaml',
    }),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/', include('api.urls')),
]
