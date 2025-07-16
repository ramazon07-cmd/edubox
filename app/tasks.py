from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Course

User = get_user_model()

@shared_task
def send_course_notification(course_id, user_id):
    user = User.objects.get(id=user_id)
    course = Course.objects.get(id=course_id)

    subject = f"You've enrolled in {course.title}"
    message = f"Hello {user.first_name},\n\nYou've successfully enrolled in {course.title}.\n\nEnjoy learning!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
