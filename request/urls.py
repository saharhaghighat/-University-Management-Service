from django.urls import path
from .views import (StudentTermRemoval,
                    AssistantTermRemoval,
                    AssistantTermRemovalList,
                    CourseSelectionRequestViewSet)

urlpatterns = [
    path('student/<int:pk>/remove-term/', StudentTermRemoval.as_view(), name='student_remove_term'),
    path('assistant/remove-term/', AssistantTermRemovalList.as_view(), name='assistant_remove_term_list'),
    path('assistant/remove-term/<int:pk>/', AssistantTermRemoval.as_view(), name='assistant_remove_term_detail'),
    path('course-selection/create/', CourseSelectionRequestViewSet.as_view({'get': 'list', 'post': 'create'}), name='course-selection-create'),
    path('course-selection/check/', CourseSelectionRequestViewSet.as_view({'post': 'check_course_conditions'}), name='check_conditions'),
    ]

