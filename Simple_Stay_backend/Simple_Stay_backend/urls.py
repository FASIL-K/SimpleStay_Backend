from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('owner/', include('owner.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('savedpost/', include('savedpost.urls')),  
    path('premium/', include('premium.urls')),  
    path('chat/', include('chat.urls')),  

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
