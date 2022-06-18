
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from apps.users.apis import auth_view

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    ]

router = DefaultRouter()

router.register(r'auth', auth_view.AuthView, basename='auth')
router.register(r'kyc', auth_view.KycView, basename='kyc')

urlpatterns += [
    path('', include(router.urls)),
]
