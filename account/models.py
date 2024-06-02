from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from department.models import Faculty, Term, Field, Course
from utils.model_helper import national_code_regex, phone_regex, user_image_path


class GenderChoices(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')


class AcademicRank(models.TextChoices):
    ASSISTANT_PROFESSOR = 'assistant_p', _('Assistant Professor')
    ASSOCIATE_PROFESSOR = 'associate_p', _('Associate Professor')
    PROFESSOR = 'full_p', _('Professor')


class UserManager(BaseUserManager):
    def _create_user(self, national_code, email, password, **extra_fields):
        if not national_code:
            raise ValueError("The given national code must be set")

        email = self.normalize_email(email)
        user = self.model(national_code=national_code, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, national_code, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(national_code, email, password, **extra_fields)

    def create_superuser(self, national_code, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(national_code, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    national_code = models.CharField(verbose_name=_("national code"), max_length=10, validators=[national_code_regex],
                                     unique=True)
    gender = models.CharField(verbose_name=_("gender"), max_length=1, choices=GenderChoices.choices)
    phone = models.CharField(verbose_name=_("phone"), max_length=11, validators=[phone_regex])
    profile_image = models.ImageField(verbose_name=_("profile image"), upload_to=user_image_path, blank=True, null=True)
    birth_date = models.DateField(verbose_name=_("birth date"), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)

    USERNAME_FIELD = 'national_code'

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _('Teachers')

    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='_teacher',
                                primary_key=True)
    faculty = models.ForeignKey(
        verbose_name=_("faculty"), to=Faculty, on_delete=models.PROTECT
    )
    field = models.ForeignKey(
        verbose_name=_("field"), to=Field, on_delete=models.PROTECT
    )
    specialization = models.CharField(verbose_name=_("specialization"), max_length=255)
    academic_rank = models.CharField(verbose_name=_("academic rank"), max_length=11, choices=AcademicRank.choices)
    taught_courses = models.ManyToManyField(
        verbose_name=_("taught courses"), to=Course, related_name="taught_courses"
    )


class Student(models.Model):
    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _('Students')

    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='_student',
                                primary_key=True)
    entry_year = models.PositiveSmallIntegerField(
        verbose_name=_("entry year"),
        validators=[
            MinValueValidator(1360),
            MaxValueValidator(1460)
        ]
    )
    entry_term = models.ForeignKey(verbose_name=_("entry term"), to=Term, on_delete=models.PROTECT)
    gpa = models.FloatField(
        verbose_name=_("gpa"),
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(20.0)
        ]
    )
    faculty = models.ForeignKey(verbose_name=_("faculty"), to=Faculty, on_delete=models.PROTECT)
    field = models.ForeignKey(verbose_name=_("field"), to=Field, on_delete=models.PROTECT)
    advisor = models.ForeignKey(verbose_name=_("advisor"), to=Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    passed_courses = models.ManyToManyField(verbose_name=_("passed courses"), to=Course, related_name='passed_courses')
    in_progress_courses = models.ManyToManyField(verbose_name=_("in progress courses"), to=Course,
                                                 related_name='in_progress_courses')
    military_service_status = models.BooleanField(verbose_name=_("military service status"), default=False)
    academic_probation_years = models.PositiveSmallIntegerField(verbose_name=_("academic probation years"),
                                                                validators=[MaxValueValidator(12)])


class EducationalAssistant(models.Model):
    class Meta:
        verbose_name = _("Assistant")
        verbose_name_plural = _('Assistants')

    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='_assistant',
                                primary_key=True)
    faculty = models.ForeignKey(
        verbose_name=_("faculty"), to=Faculty, on_delete=models.PROTECT
    )
    field = models.ForeignKey(
        verbose_name=_("field"), to=Field, on_delete=models.PROTECT
    )
