from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # app
    path('api-auth/' , include("user.urls")),
    path('api-produsts/' , include("products.urls")),
    path('api-orders2/' , include("orders2.urls")),
    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)