from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, RideViewSet, TrackingViewSet, AttendanceViewSet, NotificationViewSet, AdminDashboardViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet)
router.register(r'rides', RideViewSet)
router.register(r'tracking', TrackingViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'admin', AdminDashboardViewSet, basename='admin-dashboard')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]