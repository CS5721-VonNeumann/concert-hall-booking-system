"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Concert Hall",
        default_version='v1',
        description="Concert Hall Booking Sytem",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Sample License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("shows/", include('show_manager.urls')),
    path("hall_manager/", include('hall_manager.urls')),
    path("ticket_manager/", include('ticket_manager.urls')),
    path("notifications/", include('notifications.urls')),
    path("membership/", include('membership.urls')),
    path("payment_gateway/", include('payment_gateway.urls')),
    path('authentication/', include('users.urls')),
    path('recommendations/', include('recommendation_engine.urls')),
    path('swagger/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
]
