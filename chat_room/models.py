from django.db import models
from course.models import TimeStampMixin
from course.models import Course
from django.conf import settings 
# Create your models here.
class ChatRoom(TimeStampMixin):
    ROOM_TYPE_CHOICES = [
        ("Group", "Group"),
        ("Private", "Private"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="chat_rooms"
    )
    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPE_CHOICES
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_chat_rooms"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.title} [{self.room_type}]"


class ChatParticipant(TimeStampMixin):
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="participants"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_participations"
    )
    is_admin = models.BooleanField(default=False)  # Expert = True
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("room", "user")

    def __str__(self):
        return f"{self.user} in {self.room}"


class ChatMessage(TimeStampMixin):
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}: {self.message[:30]}"
