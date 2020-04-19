import django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('membership/', include('membership.urls')),
    path('payment/', include('payment.urls')),
    path('cart/', include('cart.urls')),
    path('', include("content.urls")),
    path('registerorder/', include('order.urls')),
    path('stores',include('stores.urls'))


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

