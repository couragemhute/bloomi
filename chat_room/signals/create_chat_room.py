# chat_room/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from course.models import Expert
from enrollment.models import CourseEnrollment
from chat_room.models import ChatRoom, ChatParticipant

@receiver(post_save, sender=CourseEnrollment)
def create_course_chat_room(sender, instance, created, **kwargs):
    if created:
        student = instance.student
        course = instance.course

        # Check if a Group chat room for this course already exists
        room, room_created = ChatRoom.objects.get_or_create(
            course=course,
            room_type="Group",
            defaults={"created_by": student}
        )

        # Add the enrolled student as a participant
        ChatParticipant.objects.get_or_create(
            room=room,
            user=student,
            defaults={"is_admin": False}
        )

        # Add all experts assigned to this course as participants
        experts = Expert.objects.filter(course=course, end_date__isnull=True)
        for expert in experts:
            ChatParticipant.objects.get_or_create(
                room=room,
                user=expert.user,
                defaults={"is_admin": True}
            )
