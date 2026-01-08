from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.utils.timezone import now


class TimeStampMixin(models.Model):
    """Reusable timestamp fields for created/updated tracking"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Course(TimeStampMixin):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to="courses/")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="beginner")
    description = models.TextField()
    overview = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def current_expert(self):
        today = now().date()
        return self.expert_assignments.filter(
            start_date__lte=today, 
            end_date__isnull=True
        ).first()

    def get_course_ratings(self):
        return self.course_ratings.all()

    def get_total_rating(self):
        total = 0
        total = self.get_course_ratings().count()
        return total
        
    def get_average_rating(self):
        total = 0
        ratings = self.get_course_ratings()
        for rating in ratings:
            total += rating.stars
        if ratings:
            return total / ratings.count()
        return 0
    

class Expert(TimeStampMixin):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="expert_assignments", null=True, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_assignments", null=True, blank=True
    )
    
    start_date = models.DateField( null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "user", "start_date"],
                name="unique_course_user_start"
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.course} ({self.start_date})"

class WhatStudentWillLearn(TimeStampMixin):
    course = models.ForeignKey(
        "Course",  
        on_delete=models.CASCADE,
        related_name="learning_outcomes"  # allows course.learning_outcomes.all()
    )
    content = models.TextField(help_text="Describe what the student will learn in this course")

    def __str__(self):
        return f"{self.course.title} → {self.content[:50]}..." 


class CourseRating(TimeStampMixin):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_ratings')
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'user') 

    def __str__(self):
        return f"{self.user.full_name} - {self.course.title} ({self.stars} Stars)"
