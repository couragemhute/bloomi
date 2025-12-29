from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from enrollment.models.academic_year import AcademicYear
from enrollment.models.class_level import ClassLevel
from enrollment.models.student_enrollment import StudentEnrollment

class Command(BaseCommand):
    help = "Create custom permissions for multiple models"

    model_permissions = [
        {
            "model": StudentEnrollment,
            "permissions": [
                ("can_promote_students", "Can promote students"),
                ("can_repeat_students", "Can mark students as repeating"),
                ("can_transfer_students", "Can transfer students"),
            ],
        },
        {
            "model": ClassLevel,
            "permissions": [
                ("can_archive_class_levels", "Can archive class levels"),
            ],
        },
        {
            "model": AcademicYear,
            "permissions": [
                ("can_close_academic_year", "Can close academic year"),
                ("can_rollback_academic_year", "Can rollback academic year"),
            ],
        },
        # Add more as needed
    ]

    def handle(self, *args, **kwargs):
        for entry in self.model_permissions:
            model = entry["model"]
            content_type = ContentType.objects.get_for_model(model)

            for codename, name in entry["permissions"]:
                permission, created = Permission.objects.get_or_create(
                    codename=codename,
                    name=name,
                    content_type=content_type,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Permission '{name}' created."))
                else:
                    self.stdout.write(self.style.WARNING(f"Permission '{name}' already exists."))
