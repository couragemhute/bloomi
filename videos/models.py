# videos/models.py
from django.db import models

class AIVideo(models.Model):
    prompt = models.TextField()
    video = models.FileField(upload_to='ai_videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video {self.id} - {self.prompt[:50]}"
