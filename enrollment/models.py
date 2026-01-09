from django.db import models
from course.models import TimeStampMixin
from course.models import Course
from django.conf import settings 

class CourseEnrollment(TimeStampMixin):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_enrollments"
    )
    is_active = models.BooleanField(default=True)
    has_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("course", "student")

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
