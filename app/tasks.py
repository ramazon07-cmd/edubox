from celery import shared_task

@shared_task
def send_course_notification(course_id):
    print(f"Sending notification for course ID: {course_id}")
