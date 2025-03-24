from datetime import timezone

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import User, Ride, Tracking, Attendance, Notification
from .serializers import UserSerializer, RideSerializer, TrackingSerializer, AttendanceSerializer, NotificationSerializer


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]  # Open endpoints
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user (Admin/Parent/Driver)"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully', 'user': UserSerializer(user).data}, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout the user by blacklisting token"""
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Retrieve logged-in user's profile"""
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        return Response({'error': 'Not authenticated'}, status=401)

    @action(detail=False, methods=['patch'])
    def profile_update(self, request):
        """Update user profile"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=200)
        return Response(serializer.errors, status=400)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['get'])
    def list_users(self, request):
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': 'User deactivated'})

    @action(detail=True, methods=['patch'])
    def reactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'message': 'User reactivated'})

    @action(detail=True, methods=['patch'])
    def assign_role(self, request, pk=None):
        user = self.get_object()
        new_role = request.data.get('role')
        if new_role not in ['admin', 'parent', 'driver']:
            return Response({'error': 'Invalid role'}, status=400)
        user.role = new_role
        user.save()
        return Response({'message': f'Role updated to {new_role}'})

    @action(detail=True, methods=['get'])
    def user_detail(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_user(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response({'message': 'User deleted'})

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['post'])
    def request_ride(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent=request.user, status='requested')
            return Response({'message': 'Ride requested successfully'}, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'])
    def my_requests(self, request):
        rides = Ride.objects.filter(parent=request.user)
        serializer = self.get_serializer(rides, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def accept(self, request, pk=None):
        ride = self.get_object()
        ride.status = 'accepted'
        ride.driver = request.user
        ride.save()
        return Response({'message': 'Ride accepted'})

    @action(detail=True, methods=['patch'])
    def start(self, request, pk=None):
        ride = self.get_object()
        ride.status = 'started'
        ride.save()
        return Response({'message': 'Ride started'})

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        ride = self.get_object()
        ride.status = 'completed'
        ride.save()
        return Response({'message': 'Ride completed'})

class TrackingViewSet(viewsets.ModelViewSet):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['post'])
    def update_location(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Location updated'}, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['get'])
    def bus_location(self, request, pk=None):
        tracking = self.get_object()
        serializer = self.get_serializer(tracking)
        return Response(serializer.data)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        attendance = self.get_object()
        attendance.check_in_time = timezone.now()
        attendance.save()
        return Response({'message': 'Check-in successful'})

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        attendance = self.get_object()
        attendance.check_out_time = timezone.now()
        attendance.save()
        return Response({'message': 'Check-out successful'})

    @action(detail=True, methods=['get'])
    def student_attendance(self, request, pk=None):
        attendance = self.get_queryset().filter(student_id=pk)
        serializer = self.get_serializer(attendance, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def attendance_by_date(self, request):
        date = request.query_params.get('date')
        attendance = self.get_queryset().filter(check_in_time__date=date)
        serializer = self.get_serializer(attendance, many=True)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['post'])
    def send_notification(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Notification sent'}, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'])
    def list_notifications(self, request):
        notifications = Notification.objects.filter(recipient=request.user)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def mark_seen(self, request, pk=None):
        notification = self.get_object()
        notification.seen = True
        notification.save()
        return Response({'message': 'Notification marked as seen'})

    @action(detail=True, methods=['delete'])
    def delete_notification(self, request, pk=None):
        notification = self.get_object()
        notification.delete()
        return Response({'message': 'Notification deleted'})

class AdminDashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        return Response({'message': 'Dashboard overview: trips today, active buses, late check-ins'})

    @action(detail=False, methods=['get'])
    def reports_attendance(self, request):
        return Response({'message': 'Attendance reports by school or student'})

    @action(detail=False, methods=['get'])
    def alerts(self, request):
        return Response({'message': 'Critical alerts (delays, safety issues)'})




