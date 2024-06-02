from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Teacher, Student, EducationalAssistant

User = get_user_model()


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'faculty', 'field', 'entry_year', 'military_service_status']
    list_filter = ['faculty', 'field', 'entry_year', 'military_service_status']
    search_fields = ['user__first_name', 'user__last_name', 'user__national_code']


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'field', 'academic_rank')
    list_filter = ('faculty', 'field', 'academic_rank')
    search_fields = ('user__first_name', 'user__last_name', 'user__id', 'faculty', 'field', 'academic_rank')


admin.site.register(Teacher, ProfessorAdmin)
admin.site.register(Student, StudentAdmin)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "national_code",
        "first_name",
        "last_name",
        "email",
        "phone",
        "is_active",
    )
    ordering = ['last_name']
    search_fields = ("last_name__icontains", "email__icontains", "phone__contains")
    fieldsets = (
        (None, {"fields": ("national_code", "password")}),
        ("Image", {"fields": ("profile_image",)}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "phone")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "birth_date")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('national_code', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.username = obj.national_code
        super().save_model(request, obj, form, change)


@admin.register(EducationalAssistant)
class EducationalAssistantAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'field',)
    list_filter = ('faculty', 'field')
    search_fields = ('user__first_name', 'user__last_name', 'user__id', 'faculty', 'field')
