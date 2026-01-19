# dashboard/utils.py

from django.db.models import Count, Avg
from accounts.models import CustomUser
from course.models import Course, CourseRating
from enrollment.models import CourseEnrollment

def get_student_dashboard_data(user):
    """
    Returns all data needed for a student dashboard
    """
    if not user.role or user.role.name != "Student":
        return None

    # Courses student is enrolled in
    enrollments = CourseEnrollment.objects.filter(student=user, is_active=True)
    total_courses = enrollments.count()

    # Completed courses
    completed_courses = enrollments.filter(has_completed=True).count()

    # Ratings by the student
    ratings = CourseRating.objects.filter(user=user)
    avg_rating = ratings.aggregate(Avg("stars"))["stars__avg"] or 0

    # Courses progress list
    courses_progress = []
    for enrollment in enrollments.select_related("course"):
        course = enrollment.course
        progress = {
            "title": course.title,
            "completed": enrollment.has_completed,
            "average_rating": course.get_average_rating(),
        }
        courses_progress.append(progress)

    # Example charts: courses completed vs pending
    chart_data = {
        "labels": ["Completed", "Pending"],
        "data": [completed_courses, total_courses - completed_courses]
    }

    return {
        "total_courses": total_courses,
        "completed_courses": completed_courses,
        "average_rating": round(avg_rating, 2),
        "courses_progress": courses_progress,
        "chart_data": chart_data,
    }

