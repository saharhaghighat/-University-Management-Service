from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import serializers

from account.models import EducationalAssistant
from .models import Faculty, Course, TermCourse, Term
from .serializers import (FacultySerializer, 
                        TermCourseSerializer,
                        CourseSerializer,
                        TermSerializer, 
                        StudentCourseSerializer)
from utils.view_helper import CustomPagination


class FacultyAPIView(APIView):
    pagination_class = CustomPagination

    def get(self, request, format=None):
        faculties = Faculty.objects.all()

        name = request.query_params.get('name', None)
        if name:
            faculties = faculties.filter(name__icontains=name)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(faculties, request)
        serializer = FacultySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacultyDetailView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request, pk, format=None):
        faculty = get_object_or_404(Faculty, pk=pk)
        serializer = FacultySerializer(faculty)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk, format=None):
        faculty = get_object_or_404(Faculty, pk=pk)
        serializer = FacultySerializer(faculty, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk, format=None):
        faculty = get_object_or_404(Faculty, pk=pk)
        faculty.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsAdminUser()]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            try:
                assistant = EducationalAssistant.objects.get(user=user)
                if assistant.faculty.pk != request.data.get('offering_faculty'):
                    raise serializers.ValidationError("You are not allowed to create course in this faculty.")
            except (ObjectDoesNotExist, TypeError):
                raise serializers.ValidationError("Authentication credentials were not provided.")
        return super().post(request, *args, **kwargs)


class CourseView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    allowed_methods = ['GET', 'PUT', 'DELETE']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAdminUser()]
        return super().get_permissions()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if not user.is_superuser:
            try:
                assistant = EducationalAssistant.objects.get(user=user)
                if assistant.faculty.pk != instance.offering_faculty.pk:
                    raise serializers.ValidationError("You are not allowed to delete course from this faculty.")
            except (ObjectDoesNotExist, TypeError):
                raise serializers.ValidationError("Authentication credentials were not provided.")
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        # check authorization of staff
        if not user.is_superuser:
            try:
                assistant = EducationalAssistant.objects.get(user=user)
                if assistant.faculty.pk != Course.objects.get(pk=instance.pk).offering_faculty.pk:
                    raise serializers.ValidationError("You are not allowed to update course in this faculty.")
            except (ObjectDoesNotExist, TypeError):
                raise serializers.ValidationError("Authentication credentials were not provided.")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TermCourseCreateView(generics.ListCreateAPIView):
    queryset = TermCourse.objects.all()
    serializer_class = TermCourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsAdminUser()]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            try:
                assistant = EducationalAssistant.objects.get(user=user)
                if assistant.faculty.pk != request.data.get('offering_faculty'):
                    raise serializers.ValidationError("You are not allowed to create term course in this faculty.")
            except (ObjectDoesNotExist, TypeError):
                raise serializers.ValidationError("Authentication credentials were not provided.")
        return super().post(request, *args, **kwargs)


class TermCourseView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TermCourse.objects.all()
    serializer_class = TermCourseSerializer
    allowed_methods = ['GET', 'PUT', 'DELETE']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAdminUser()]
        return super().get_permissions()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if not user.is_superuser:
            try:
                assistant = EducationalAssistant.objects.get(user=user)
                if assistant.faculty.pk != instance.offering_faculty.pk:
                    raise serializers.ValidationError("You are not allowed to delete term course from this faculty.")
            except (ObjectDoesNotExist, TypeError):
                raise serializers.ValidationError("Authentication credentials were not provided.")
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        # check authorization of staff
        if not user.is_superuser:
            try:
                assistant = EducationalAssistant.objects.get(user=user)
                if assistant.faculty.pk != TermCourse.objects.get(pk=instance.pk).offering_faculty.pk:
                    raise serializers.ValidationError("You are not allowed to update term course in this faculty.")
            except (ObjectDoesNotExist, TypeError):
                raise serializers.ValidationError("Authentication credentials were not provided.")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class TermListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TermSerializer
    pagination_class = CustomPagination
    queryset = Term.objects.all()

class TermRetrieveUpdateDestroyAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Term.objects.all()
    serializer_class = TermSerializer

class AvailableCoursesAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        student = self.request.user._student
        taken_courses = student.passed_courses.all() | student.in_progress_courses.all()

        all_courses = Course.objects.all()

        available_courses = []
        for course in all_courses:
            if taken_courses.filter(pk__in=course.prerequisites_courses.all()).exists() or \
               taken_courses.filter(pk__in=course.corequisites_courses.all()).exists():
                available_courses.append(course)

        return available_courses

class StudentPassedCoursesAPIView(generics.ListAPIView):
    serializer_class = StudentCourseSerializer

    def get_queryset(self):
        student = self.request.user._student
        return student.student_courses.all()