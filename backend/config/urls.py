from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import CustomTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain"),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.fleet.urls")),
    path("api/v1/", include("apps.emergencies.urls")),
    path("api/v1/", include("apps.payments.urls")),
    path("api/v1/", include("apps.notifications.urls")),
    path("api/v1/", include("apps.ai.urls")),
    path("api/v1/", include("apps.ota.urls")),
    path("api/v1/", include("apps.integrations.urls")),
    path("api/v1/admin-panel/", include("apps.accounts.admin_panel_urls")),
    path("api/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
