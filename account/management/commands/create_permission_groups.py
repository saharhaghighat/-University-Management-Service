from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from samane_golestan.settings import ASSISTANTS_GROUP_NAME

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            assistants_group = Group.objects.get(name=ASSISTANTS_GROUP_NAME)
            assistants_group.delete()
        except Group.DoesNotExist:
            pass
        finally:
            assistants_group = Group.objects.create(name=ASSISTANTS_GROUP_NAME)

        can_add_course = Permission.objects.get(codename="add_course")
        can_change_course = Permission.objects.get(codename="change_course")
        can_delete_course = Permission.objects.get(codename="delete_course")
        can_view_course = Permission.objects.get(codename="view_course")

        can_add_term_course = Permission.objects.get(codename="add_termcourse")
        can_change_term_course = Permission.objects.get(codename="change_termcourse")
        can_delete_term_course = Permission.objects.get(codename="delete_termcourse")
        can_view_term_course = Permission.objects.get(codename="view_termcourse")

        can_view_teacher = Permission.objects.get(codename="view_teacher")

        can_view_student = Permission.objects.get(codename="view_student")

        can_view_term_deletion_request = Permission.objects.get(codename="view_termdeletionrequest")
        can_change_term_deletion_request = Permission.objects.get(codename="change_termdeletionrequest")

        can_view_studying_certificate_request = Permission.objects.get(codename="view_studyingcertificaterequest")
        can_change_studying_certificate_request = Permission.objects.get(codename="change_studyingcertificaterequest")

        can_view_review_request = Permission.objects.get(codename="view_review")
        can_change_review_request = Permission.objects.get(codename="change_review")

        can_view_emergency_deletion_request = Permission.objects.get(codename="view_emergencydeletionrequest")
        can_change_emergency_deletion_request = Permission.objects.get(codename="change_emergencydeletionrequest")

        assistants_group.permissions.add(can_add_course)
        assistants_group.permissions.add(can_change_course)
        assistants_group.permissions.add(can_delete_course)
        assistants_group.permissions.add(can_view_course)
        assistants_group.permissions.add(can_add_term_course)
        assistants_group.permissions.add(can_change_term_course)
        assistants_group.permissions.add(can_delete_term_course)
        assistants_group.permissions.add(can_view_term_course)
        assistants_group.permissions.add(can_view_teacher)
        assistants_group.permissions.add(can_view_student)
        assistants_group.permissions.add(can_view_term_deletion_request)
        assistants_group.permissions.add(can_change_term_deletion_request)
        assistants_group.permissions.add(can_view_studying_certificate_request)
        assistants_group.permissions.add(can_change_studying_certificate_request)
        assistants_group.permissions.add(can_view_review_request)
        assistants_group.permissions.add(can_change_review_request)
        assistants_group.permissions.add(can_view_emergency_deletion_request)
        assistants_group.permissions.add(can_change_emergency_deletion_request)

        for user in User.objects.all():
            if user.is_staff or user.is_superuser:
                user.save()
