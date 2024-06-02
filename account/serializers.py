from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Teacher, EducationalAssistant, Student

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            "id",
            "national_code",
            "gender",
            "phone",
            "profile_image",
            "birth_date",
            "password",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('user', 'faculty', 'field', 'academic_rank')
        
    def create(self, validated_data):
        teacher = Teacher.objects.create(**validated_data) 
        return teacher
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        
        if user_data:
            user_data.pop('national_code', None)

            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        
        instance.faculty = validated_data.get('faculty', instance.faculty)
        instance.field = validated_data.get('field', instance.field)
        instance.academic_rank = validated_data.get('academic_rank', instance.academic_rank)
        
        instance.save()
        return instance


class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalAssistant
        fields = ['user', 'faculty', 'field',]
    
    def create(self, validated_data):
        assist = EducationalAssistant.objects.create(**validated_data) 
        return assist
        

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user', 'faculty', 'field',]
    
    def create(self, validated_data):
        student = Student.objects.create(**validated_data) 
        return student
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        
        if user_data:
            user_data.pop('national_code', None)

            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        
        instance.faculty = validated_data.get('faculty', instance.faculty)
        instance.field = validated_data.get('field', instance.field)
        instance.academic_rank = validated_data.get('academic_rank', instance.academic_rank)
        
        instance.save()
        return instance
    


    

