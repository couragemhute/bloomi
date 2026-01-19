from django.db.models import Avg, Count
from django.utils.timezone import now

from course.models import Course, CourseRating, Expert
from enrollment.models import CourseEnrollment
from chat_room.models import ChatRoom, ChatMessage


def get_facilitator_dashboard_data(user):
    """
    Returns a dictionary with EVERYTHING related to a facilitator:
    - Courses
    - Students
    - Ratings
    - Chat activity
    - Chart-ready datasets
    """

    today = now().date()

    # 1. Assigned courses (active)
    expert_assignments = Expert.objects.filter(
        user=user,
        start_date__lte=today,
        end_date__isnull=True
    ).select_related("course")

    courses = [ea.course for ea in expert_assignments]

    # 2. Enrollments
    enrollments = CourseEnrollment.objects.filter(
        course__in=courses,
        is_active=True
    )

    total_students = enrollments.count()

    students_per_course = (
        enrollments
        .values("course__title")
        .annotate(count=Count("id"))
    )

    # 3. Ratings
    ratings = CourseRating.objects.filter(course__in=courses)

    avg_rating = ratings.aggregate(avg=Avg("stars"))["avg"] or 0

    ratings_per_course = (
        ratings
        .values("course__title")
        .annotate(avg=Avg("stars"), total=Count("id"))
    )

    # 4. Chat rooms & messages
    chat_rooms = ChatRoom.objects.filter(course__in=courses, is_active=True)

    sent_messages = ChatMessage.objects.filter(sender=user).count()

    unread_messages = ChatMessage.objects.filter(
        room__in=chat_rooms,
        is_read=False
    ).exclude(sender=user).count()

    # 5. CHART DATA (READY FOR JS)
    charts = {
        "students_per_course": {
            "labels": [item["course__title"] for item in students_per_course],
            "data": [item["count"] for item in students_per_course],
        },
        "ratings_per_course": {
            "labels": [item["course__title"] for item in ratings_per_course],
            "data": [round(item["avg"] or 0, 1) for item in ratings_per_course],
        },
    }

    return {
        # Core data
        "facilitator_courses": courses,
        "expert_assignments": expert_assignments,

        # Metrics
        "total_courses": len(courses),
        "total_students": total_students,
        "average_rating": round(avg_rating, 1),
        "sent_messages": sent_messages,
        "unread_messages": unread_messages,

        # Chat
        "chat_rooms": chat_rooms,

        # Charts
        "charts": charts,
    }
