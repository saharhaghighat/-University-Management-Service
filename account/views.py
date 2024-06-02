from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.shortcuts import get_object_or_404


from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from utils.view_helper import CustomPagination
from .models import Teacher, EducationalAssistant, Student
from .serializers import TeacherSerializer, AssistantSerializer
from account.serializers import UserRegistrationSerializer
from account.serializers import StudentSerializer

User = get_user_model()


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []


class CreateTeacherView(APIView):
    permission_classes = [permissions.IsAdminUser]
    pagination_class = CustomPagination
    serializer_class = TeacherSerializer

    def get(self, request, format=None):
        name = request.query_params.get('name')
        last_name = request.query_params.get('last_name')
        teacher_id = request.query_params.get('teacher_id')
        national_code = request.query_params.get('national_code')
        faculty = request.query_params.get('faculty')
        field = request.query_params.get('field')
        academic_rank = request.query_params.get('academic_rank')

        queryset = Teacher.objects.all()
        if name:
            queryset = queryset.filter(first_name__icontains=name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if teacher_id:
            queryset = queryset.filter(id=teacher_id)
        if national_code:
            queryset = queryset.filter(national_code=national_code)
        if faculty:
            queryset = queryset.filter(faculty__name=faculty)
        if field:
            queryset = queryset.filter(field__name=field)
        if academic_rank:
            queryset = queryset.filter(academic_rank=academic_rank)

        serializer = TeacherSerializer(queryset, many=True)

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = TeacherSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk, format=None):
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        teacher = get_object_or_404(Teacher, pk=pk)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateAssistantView(CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    pagination_class = CustomPagination
    serializer_class = AssistantSerializer

    def post(self, request, *args, **kwargs):
        serializer = AssistantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        first_name = request.query_params.get('first_name')
        last_name = request.query_params.get('last_name')
        national_code = request.query_params.get('national_code')
        faculty = request.query_params.get('faculty')
        field = request.query_params.get('field')

        queryset = EducationalAssistant.objects.all()
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if national_code:
            queryset = queryset.filter(national_code=national_code)
        if faculty:
            queryset = queryset.filter(faculty__name=faculty)
        if field:
            queryset = queryset.filter(field__name=field)

        serializer = AssistantSerializer(queryset, many=True)

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = AssistantSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class AssistantDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk, format=None):
        assistant = get_object_or_404(EducationalAssistant, pk=pk)
        serializer = AssistantSerializer(assistant)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        assistant = get_object_or_404(EducationalAssistant, pk=pk)
        serializer = AssistantSerializer(assistant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        assistant = get_object_or_404(EducationalAssistant, pk=pk)
        assistant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        last_name = self.request.query_params.get('last_name')
        student_id = self.request.query_params.get('student_id')
        national_code = self.request.query_params.get('national_code')
        faculty = self.request.query_params.get('faculty')
        field = self.request.query_params.get('field')
        entry_year = self.request.query_params.get('entry_year')
        military_service_status = self.request.query_params.get('military_service_status')

        if name:
            queryset = queryset.filter(first_name__icontains=name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if student_id:
            queryset = queryset.filter(id=student_id)
        if national_code:
            queryset = queryset.filter(national_code=national_code)
        if faculty:
            queryset = queryset.filter(faculty__name=faculty)
        if field:
            queryset = queryset.filter(field__name=field)
        if entry_year:
            queryset = queryset.filter(entry_year=entry_year)
        if military_service_status is not None:
            queryset = queryset.filter(military_service_status=military_service_status)

        return queryset


class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class StudentUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    
    def put(self, request, pk, format=None):
        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer

    def put(self, request, pk, format=None):
        teacher = Teacher.objects.get(pk=pk)
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomLogoutView(TokenViewBase):
    def post(self, request, *args, **kwargs):
        try:
            self.blacklist(request)
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
