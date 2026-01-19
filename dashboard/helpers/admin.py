from django.db.models import Count, Avg
from django.utils.timezone import now, timedelta

from accounts.models import CustomUser
from course.models import Course, Expert, CourseRating
from chat_room.models import ChatRoom, ChatMessage
from enrollment.models import CourseEnrollment


def get_admin_dashboard_data(user):
    """
    Returns global dashboard data for:
    - Super Admin
    - Administrator
    """

    today = now().date()
    thirty_days_ago = today - timedelta(days=30)

    # ---------------- USERS ----------------
    users = CustomUser.objects.all()

    total_users = users.count()
    facilitators = users.filter(role__name="Facillitator").count()
    students = users.exclude(role__name="Facillitator").count()

    # ---------------- COURSES ----------------
    courses = Course.objects.filter(is_active=True)

    total_courses = courses.count()

    courses_by_level = (
        courses
        .values("level")
        .annotate(count=Count("id"))
    )

    # ---------------- ENROLLMENTS ----------------
    enrollments = CourseEnrollment.objects.filter(is_active=True)

    total_enrollments = enrollments.count()

    enrollments_per_course = (
        enrollments
        .values("course__title")
        .annotate(count=Count("id"))
    )

    # ---------------- RATINGS ----------------
    ratings = CourseRating.objects.all()
    avg_rating = ratings.aggregate(avg=Avg("stars"))["avg"] or 0

    ratings_per_course = (
        ratings
        .values("course__title")
        .annotate(avg=Avg("stars"))
    )

    # ---------------- CHAT ----------------
    chat_rooms = ChatRoom.objects.filter(is_active=True)
    total_chat_rooms = chat_rooms.count()

    messages_last_30_days = ChatMessage.objects.filter(
        created_at__date__gte=thirty_days_ago
    ).count()

    # ---------------- CHART DATA ----------------
    charts = {
        "courses_by_level": {
            "labels": [item["level"].title() for item in courses_by_level],
            "data": [item["count"] for item in courses_by_level],
        },
        "enrollments_per_course": {
            "labels": [item["course__title"] for item in enrollments_per_course],
            "data": [item["count"] for item in enrollments_per_course],
        },
        "ratings_per_course": {
            "labels": [item["course__title"] for item in ratings_per_course],
            "data": [round(item["avg"] or 0, 1) for item in ratings_per_course],
        },
    }

    return {
        # USERS
        "total_users": total_users,
        "facilitators": facilitators,
        "students": students,

        # COURSES
        "total_courses": total_courses,

        # ENROLLMENTS
        "total_enrollments": total_enrollments,

        # RATINGS
        "average_rating": round(avg_rating, 1),

        # CHAT
        "total_chat_rooms": total_chat_rooms,
        "messages_last_30_days": messages_last_30_days,

        # CHARTS
        "charts": charts,
    }
