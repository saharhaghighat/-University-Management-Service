from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class CourseType(models.TextChoices):
    OPTIONAL = 'optional', _('Optional')
    BASIC = 'basic', _('Basic')
    GENERAL = 'general', _('General')
    SPECIALIZED = 'specialized', _('Specialized')
    PRACTICAL = 'practical', _('Practical')


class Faculty(models.Model):
    class Meta:
        verbose_name = _("faculty")
        verbose_name_plural = _("faculties")

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Term(models.Model):
    class Meta:
        verbose_name = _("term")
        verbose_name_plural = _("terms")

    name = models.CharField(verbose_name=_("name"), max_length=50)
    class_start = models.DateTimeField(verbose_name=_("class start"))
    class_end = models.DateTimeField(verbose_name=_("class end"))
    enrollment_start = models.DateTimeField(verbose_name=_("enrollment start"))
    enrollment_end = models.DateTimeField(verbose_name=_("enrollment end"))
    amend_start = models.DateTimeField(verbose_name=_("amend start"))
    amend_end = models.DateTimeField(verbose_name=_("amend end"))
    emergency_drop_end = models.DateTimeField(verbose_name=_("emergency drop end"))
    exam_start = models.DateTimeField(verbose_name=_("exam start"))
    term_end = models.DateTimeField(verbose_name=_("term end"))

    def __str__(self):
        return self.name


class Field(models.Model):
    class Meta:
        verbose_name = _("field")
        verbose_name_plural = _("fields")

    GRADE_CHOICES = [
        ('bachelor', _('Bachelor')),
        ('master', _('Master')),
        ('doctorate', _('Doctorate')),
    ]
    name = models.CharField(max_length=40)
    academic_department = models.CharField(max_length=20)
    department = models.ForeignKey(to=Faculty, on_delete=models.CASCADE)
    credit_numbers = models.PositiveIntegerField(validators=[MaxValueValidator(200)])
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)

    def __str__(self):
        return self.name


class CourseType(models.TextChoices):
    OPTIONAL = 'optional', _('Optional')
    BASIC = 'basic', _('Basic')
    GENERAL = 'general', _('General')
    SPECIALIZED = 'specialized', _('Specialized')
    OTHER = 'other', _('Other')


class Course(models.Model):
    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    name = models.CharField(verbose_name=_("name"), max_length=30)
    offering_faculty = models.ForeignKey(verbose_name=_("offering faculty"), to=Faculty, on_delete=models.SET_NULL,
                                         null=True, blank=True)
    prerequisites_courses = models.ManyToManyField('self', verbose_name=_("prerequisites courses"), symmetrical=False,
                                                   related_name='prerequisites', blank=True)
    corequisites_courses = models.ManyToManyField('self', verbose_name=_("corequisites courses"), symmetrical=False,
                                                  related_name='corequisites', blank=True)
    units = models.PositiveSmallIntegerField(verbose_name=_("units"), choices=[(i, i) for i in range(1, 5)])
    type = models.CharField(verbose_name=_("type"), max_length=100, choices=CourseType.choices)

    def __str__(self):
        return self.name


class TermCourse(models.Model):
    class Meta:
        verbose_name = _("term course")
        verbose_name_plural = _("term courses")

    DAY_CHOICES = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
        ("SUN", "Sunday"),
    ]
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_date = models.DateTimeField(null=True, blank=True)
    exam_location = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(to='account.Teacher', on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    term = models.ForeignKey(Term, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.term.name} - {self.course.name}"


class StudentCourse(models.Model):
    class Meta:
        verbose_name = "student course"
        verbose_name_plural = "student courses"

    COURSE_STATUS_CHOICES = (
        ('started', _('Started')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
    )
    student = models.ForeignKey(to='account.Student', on_delete=models.CASCADE)
    course_status = models.CharField(max_length=20, choices=COURSE_STATUS_CHOICES)
    student_score = models.FloatField(validators=[
        MinValueValidator(0.0),
        MaxValueValidator(20.0)
    ])
    term = models.ForeignKey(to=Term, on_delete=models.CASCADE)

    def __str__(self):
        return f"Course status: {self.get_course_status_display()}"
