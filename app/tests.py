from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Course

User = get_user_model()


class CourseModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python for Beginners",
            description="Learn Python programming from scratch",
            price=Decimal("29.99")
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    def test_course_creation(self):
        """Test that course is created with correct attributes"""
        self.assertEqual(self.course.title, "Python for Beginners")
        self.assertEqual(self.course.description, "Learn Python programming from scratch")
        self.assertEqual(self.course.price, Decimal("29.99"))
        self.assertEqual(str(self.course), "Python for Beginners")

    def test_course_enrollment(self):
        """Test student enrollment in a course"""
        self.assertEqual(self.course.students.count(), 0)
        self.course.students.add(self.user)
        self.assertEqual(self.course.students.count(), 1)
        self.assertTrue(self.user in self.course.students.all())


class CourseAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123"
        )
        self.course = Course.objects.create(
            title="Python for Beginners",
            description="Learn Python programming from scratch",
            price=Decimal("29.99")
        )
        self.course_data = {
            "title": "Django for Beginners",
            "description": "Learn Django framework fundamentals",
            "price": "39.99"
        }

    def test_get_courses_list(self):
        """Test retrieving a list of courses"""
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_course_detail(self):
        """Test retrieving a specific course"""
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.course.title)

    def test_create_course_unauthorized(self):
        """Test that unauthorized users cannot create courses"""
        url = reverse('course-list')
        response = self.client.post(url, self.course_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_course_authorized(self):
        """Test course creation by authorized user"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('course-list')
        response = self.client.post(url, self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.get(id=2).title, "Django for Beginners")

    def test_enroll_in_course(self):
        """Test enrolling in a course"""
        self.client.force_authenticate(user=self.user)
        url = reverse('course-enroll', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user in self.course.students.all())

    def test_enroll_in_course_twice(self):
        """Test that enrolling twice returns an error"""
        self.client.force_authenticate(user=self.user)
        url = reverse('course-enroll', args=[self.course.id])
        # First enrollment
        self.client.post(url)
        # Second enrollment attempt
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.course.students.count(), 1)

    def test_update_course(self):
        """Test updating a course"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('course-detail', args=[self.course.id])
        updated_data = {
            "title": "Updated Python Course",
            "description": self.course.description,
            "price": self.course.price
        }
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated Python Course")

    def test_delete_course(self):
        """Test deleting a course"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)