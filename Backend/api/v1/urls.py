from django.urls import include, path
from ..routers import router
from .viewsets import KanbanAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', KanbanAPIView.as_view(), name='api-dashboard'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]