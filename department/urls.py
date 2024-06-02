from django.urls import path

from .views import (TermCourseCreateView,
                     TermCourseView,
                    CourseCreateView,
                    CourseView,
                    TermListCreateAPIView, 
                    TermRetrieveUpdateDestroyAPIView,
                    AvailableCoursesAPIView)

urlpatterns = [
    path('subjects/', CourseCreateView.as_view(), name='course-list-create'),
    path('subjects/<int:pk>/', CourseView.as_view(), name='course-retrieve-update-destroy'),
    path('courses/', TermCourseCreateView.as_view(), name='term-course-list-create'),
    path('courses/<int:pk>/', TermCourseView.as_view(), name='term-course-retrieve-update-destroy'),
    path('terms/', TermListCreateAPIView.as_view(), name='term-list-create'),
    path('terms/<int:pk>/', TermRetrieveUpdateDestroyAPIView.as_view(), name='term-retrieve-update-destroy'),
    path('student/my-courses/', AvailableCoursesAPIView.as_view(), name='available-courses'),
    path('student/pass-courses-report/', AvailableCoursesAPIView.as_view(), name='pass-courses-report'),
]