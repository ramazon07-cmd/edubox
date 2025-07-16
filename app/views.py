# views.py

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer
from .tasks import send_course_notification

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        method='post',
        operation_description="Kursga yozilish",
        responses={200: openapi.Response("Yozildi"), 400: "Allaqachon yozilgan"},
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        user = request.user
        if course.students.filter(id=user.id).exists():
            return Response({'detail': 'Already enrolled'}, status=status.HTTP_400_BAD_REQUEST)

        course.students.add(user)
        send_course_notification.delay(course.id, user.id)
        return Response({'detail': 'Enrolled successfully! ✅'})
