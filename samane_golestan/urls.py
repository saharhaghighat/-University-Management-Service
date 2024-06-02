"""
URL configuration for samane_golestan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from account.views import (CreateTeacherView,
                           TeacherDetailView,
                           CreateAssistantView,
                           AssistantDetailView,
                           StudentUpdateView,
                           TeacherUpdateView)
from department.views import FacultyAPIView, FacultyDetailView

urlpatterns = [
    path('admin/professors/', CreateTeacherView.as_view()),
    path('admin/professors/<str:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('admin/assistants/', CreateAssistantView.as_view()),
    path('admin/assistants/<str:pk>/', AssistantDetailView.as_view(), name='assistant_detail'),
    path('admin/faculties/', FacultyAPIView.as_view(), name='faculties'),
    path('admin/faculty/<int:pk>/', FacultyDetailView.as_view(), name='faculty_admin_api'),
    path("admin/", admin.site.urls),
    path('students/<int:pk>/', StudentUpdateView.as_view(), name='update_student'),
    path('professors/<int:pk>/', TeacherUpdateView.as_view(), name='update_teacher'),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/", include("account.urls")),
    path("api/", include("department.urls")),
    path("api/", include("request.urls")),
]
