from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

from .models import Student, TermDeletionRequest, Enrollment
from .serializers import (TermDeletionRequestSerializer,
                        AssistantTermRemovalSerializer,
                        EnrollmentSerializer)
from department.models import Course, TermCourse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery import shared_task


class StudentTermRemoval(CreateAPIView):
    queryset = TermDeletionRequest.objects.all()
    serializer_class = TermDeletionRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TermDeletionRequest.objects.filter(student=self.request.user._student)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TermDeletionRequestSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk, format=None):
        serializer = TermDeletionRequestSerializer(data=request.data, context={'request': request}) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(student=request.user._student)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class AssistantTermRemoval(APIView):
    permission_classes = []
    serializer_class = TermDeletionRequestSerializer
    
    def get(self, request, pk, *args, **kwargs):
        try:
            term_deletion_request = TermDeletionRequest.objects.get(id=pk)
        except TermDeletionRequest.DoesNotExist:
            return Response({"error": "Term deletion request not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssistantTermRemovalSerializer(term_deletion_request)

        return Response(serializer.data)

    def post(self, request, pk, format=None):
        
        
        try:
            term_deletion_request = TermDeletionRequest.objects.get(id=pk)
        except TermDeletionRequest.DoesNotExist:
            return Response({"error": "Term deletion request not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AssistantTermRemovalSerializer(term_deletion_request, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AssistantTermRemovalList(APIView):
    permission_classes = []
    serializer_class = TermDeletionRequestSerializer
    
    def get(self, request, *args, **kwargs):
        term_deletion_requests = TermDeletionRequest.objects.all()
        serializer = AssistantTermRemovalSerializer(term_deletion_requests, many=True)

        return Response(serializer.data)
from rest_framework.decorators import action

class CourseSelectionRequestViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = request.user._student
        course_id = serializer.validated_data.get('course')

        if Enrollment.objects.filter(student=student, course=course_id).exists():
            return Response({"detail": "You are already enrolled in this course."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(student=student, status='pending')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def check_course_conditions(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        
        selected_courses = request.queryset.get('selected_courses', [])

        student = request.user._student

        errors = []

        for course_id in selected_courses:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                errors.append(f"Course with ID '{course_id}' does not exist.")
                continue

            if not Enrollment.objects.filter(student=student, course=course, status='accepted').exists():
                errors.append(f"Prerequisite course '{course.name}' must be in accepted status.")

            corequisites = course.corequisites.all()
            for corequisite in corequisites:
                if not Enrollment.objects.filter(student=student, course=corequisite, status='accepted').exists():
                    errors.append(f"Prerequisite course '{corequisite.name}' must be in accepted status.")

        existing_courses = Enrollment.objects.filter(student=student, course__in=selected_courses, status='accepted')
        for existing_course in existing_courses:
            errors.append(f"Course '{existing_course.course.name}' is already passed and cannot be selected.")

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "All conditions are met."}, status=status.HTTP_200_OK)
    