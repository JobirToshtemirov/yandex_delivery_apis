from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('app_common.urls')),
    path('api/superadmin/', include('app_admin.urls')),
    path('api/user/', include('app_users.urls')),
    path('api/basket/', include('app_basket.urls')),
    # path('api/order/', include('app_order.urls')),
    # path('api/product/', include('app_products.urls')),
    path('api/restaurant/', include('app_company.urls')),
    path('api/branch/', include('app_branch.urls')),
    path('api/courier/', include('app_courier.urls')),
]

# JWT Authentication
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="This is a sample server.  You can find out more about Swagger at "
                    "[http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/). "
                    "For this sample, you can use the api key `special-key` to test the authorization filters.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="alamovasad@gmail.com", url="https://alamovasadbek.vercel.app/",
                                name="Alamov Asadbek"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
