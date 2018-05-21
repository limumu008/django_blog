from django.urls import path

from . import views

app_name = 'course'
urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('create/', views.CreateCourseView.as_view(), name='course_create'),
    path('update/<int:pk>/', views.UpdateCourseView.as_view(), name='course_update'),
    path('delete/<int:pk>/', views.DeleteCourseView.as_view(), name='course_delete'),
]
