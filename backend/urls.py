from django.urls import path, include
from rest_framework import routers
from .api import views
from django.urls import path

# ViewSet router
router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('filter-group', views.FilterGroupViewSet)
router.register('filter-item', views.FilterItemViewSet)

urlpatterns = [
    path('api/auth/login/', views.login),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/tweets', views.list_tweets),
    path('api/', include(router.urls)),
]
