from django.db import models
from django.utils.text import gettext_lazy as _

from account.models import Student
from department.models import TermCourse, Term, Course


class RequestStatus(models.TextChoices):
    ACCEPTED = 'approved', _('Approved')
    REJECTED = 'rejected', _('Rejected')
    PENDING = 'pending', _('Pending')


class AmendType(models.TextChoices):
    REGISTERED = 'registered', _('Registered')
    DROPPED = 'dropped', _('Dropped')
    WAITLISTED = 'waitlisted', _('Waitlisted')


class Enrollment(models.Model):
    class Meta:
        verbose_name = _("enrollment")
        verbose_name_plural = _("enrollments")

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(TermCourse, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=RequestStatus.choices, default=RequestStatus.PENDING)

    def __str__(self):
        return f'{self.student} - {self.course} - {self.get_status_display()}'


class Amend(models.Model):
    class Meta:
        verbose_name = _("amend")
        verbose_name_plural = _("amends")

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(TermCourse, on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_("amend type"), max_length=12, choices=AmendType.choices)
    status = models.CharField(verbose_name=_("request status"), max_length=10, choices=RequestStatus.choices,
                              default=RequestStatus.PENDING)

    def __str__(self):
        return f'Amend request by {self.student} - {self.course} -> {self.get_type_display()}, status: {self.get_status_display()}'


class TermDeletionRequest(models.Model):
    class Meta:
        verbose_name = _("Term Deletion Request")
        verbose_name_plural = _("Term Deletion Requests")

    WITH_CREDITS = 'With Credits'
    WITHOUT_CREDITS = 'Without Credits'

    RESULT_CHOICES = [
        (WITH_CREDITS, _('With Credits')),
        (WITHOUT_CREDITS, _('Without Credits')),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='deletion_requests')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='deletion_requests')
    result = models.CharField(max_length=100, choices=RESULT_CHOICES, verbose_name=_('Result'))
    student_comment = models.TextField(blank=True, null=True, verbose_name=_('Student Comment'))
    academic_affairs_comment = models.TextField(blank=True, null=True, verbose_name=_('Academic Affairs Comment'))
    
    def save(self, *args, **kwargs):
        if self.result == self.WITH_CREDITS:
            self.student.academic_probation_years += 1
            self.student.save()  

        super().save(*args, **kwargs)  

    def __str__(self):
        return f'Deletion Request for {self.term} by {self.student}'

class Review(models.Model):
    class Meta:
        verbose_name = _("review")
        verbose_name_plural = _("reviews")

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(TermCourse, on_delete=models.CASCADE)
    request_text = models.TextField(verbose_name=_("request text"), blank=True, null=True)
    answer_text = models.TextField(verbose_name=_("answer text"), blank=True, null=True)
    is_reviewed = models.BooleanField(verbose_name=_("is reviewed"), default=False)

    def __str__(self):
        return f'Review request by {self.student}: {self.course} -> {self.request_text}'


class StudyingCertificateRequest(models.Model):
    class Meta:
        verbose_name = _("Studying Certificate")
        verbose_name_plural = _("Studying Certificates")

    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    term = models.ForeignKey(verbose_name=_("term"), to=Term, on_delete=models.CASCADE)
    document = models.FileField(verbose_name=_("document"), upload_to='study_files/')
    certificate_issue_place = models.CharField(verbose_name=_("certificate issue place"), max_length=255)

    def __str__(self):
        return f'Studying Certificate Request for {self.student}'


class EmergencyDeletionRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    result = models.CharField(max_length=10, choices=RequestStatus.choices, default=RequestStatus.PENDING)
    student_comment = models.TextField(blank=True, null=True)
    academic_affairs_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Emergency Deletion Request for {self.course} by {self.student}'
