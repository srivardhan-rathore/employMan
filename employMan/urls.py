from django.contrib import admin
from django.urls import path, include
from social_django.urls import urlpatterns as social_django_urlpatterns

app_name = 'accounts'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('auth/', include('social_django.urls', namespace='social')),
]

urlpatterns += social_django_urlpatterns
