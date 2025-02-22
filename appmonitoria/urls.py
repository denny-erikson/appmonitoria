"""
URL configuration for appmonitoria project.

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
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, ProfileViewSet, RoleViewSet
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from events.views import AvailabilityViewSet, CancellationViewSet, EventViewSet, ProductViewSet, ResortViewSet, TeamViewSet
from monitoria.views import (
    AddressViewSet, BankAccountViewSet, DocumentsViewSet, LocationViewSet,
    UniformViewSet, PaymentViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'Role', RoleViewSet)

router.register(r'location', LocationViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'bank_accounts', BankAccountViewSet)
router.register(r'Document', DocumentsViewSet)
router.register(r'Uniform', UniformViewSet)
router.register(r'payments', PaymentViewSet)

router.register(r'events', EventViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'cancellations', CancellationViewSet)
router.register(r'products', ProductViewSet)
router.register(r'resorts', ResortViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('events/', include('events.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)