from django.contrib import admin
from .models import Term, Course, Field, Faculty, TermCourse

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_start', 'class_end', 'enrollment_start', 'enrollment_end', 'amend_start', 'amend_end', 'emergency_drop_end', 'exam_start', 'term_end')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'offering_faculty', 'units', 'type')
    list_filter = ('offering_faculty', 'units', 'type')
    search_fields = ('name', 'offering_faculty__name')
    

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TermCourse)
class TermCourseAdmin(admin.ModelAdmin):
    list_display = ('get_course_name', 'term', 'teacher', 'capacity', 'day', 'start_time', 'exam_date')
    list_filter = ('term__name', 'course', 'teacher')
    search_fields = ('course__name', 'exam_date')

    def get_course_name(self, obj):
        return obj.course.name

    get_course_name.short_description = 'Course Name'


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade', 'department', 'academic_department', 'credit_numbers')
    list_filter = ('grade', 'department', 'academic_department')
    search_fields = ('name',)
