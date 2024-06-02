from rest_framework import serializers
from .models import TermDeletionRequest, Enrollment

class TermDeletionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermDeletionRequest
        fields = '__all__'
        
    def create(self, validated_data):
        student = self.context['request'].user._student
        
        # existing_request = TermDeletionRequest.objects.filter(student=student, result__in=[TermDeletionRequest.PENDING, TermDeletionRequest.ACCEPTED])
        # if existing_request.exists():
        #     raise serializers.ValidationError("You already have a pending or approved removal request.")
        
        return TermDeletionRequest.objects.create(
            student=student,
            student_comment=validated_data.get('student_comment'),
            term=validated_data.get('term')
        )

    def update(self, instance, validated_data):
        instance.student_comment = validated_data.get('student_comment', instance.student_comment)
        instance.term = validated_data.get('term', instance.term)
        instance.save()
        return instance

class AssistantTermRemovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermDeletionRequest
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.result = validated_data.get('result', instance.result)
        instance.academic_affairs_comment = validated_data.get('academic_affairs_comment', instance.academic_affairs_comment)
        instance.save()
        return instance

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status']