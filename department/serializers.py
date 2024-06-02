from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Faculty, Term, TermCourse, Course, CourseType, StudentCourse

User = get_user_model()


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class TermCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermCourse
        fields = '__all__'

    def validate_term(self, value):
        now = timezone.now()
        if value.amend_end < now:
            raise serializers.ValidationError("The registration period for semester courses has ended.")
        return value

    def validate(self, attrs):
        if attrs['course'].type == CourseType.PRACTICAL:
            attrs['exam_date'] = None
            attrs['exam_location'] = None
        else:
            if not attrs['exam_date']:
                raise serializers.ValidationError({'exam_date': 'Detect exam date!'})
            if not attrs['exam_location']:
                raise serializers.ValidationError({'exam_location': 'Detect exam location!'})
        return attrs


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'

class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = '__all__'

