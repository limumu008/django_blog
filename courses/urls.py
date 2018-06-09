from django.urls import path

from . import views

app_name = 'course'
urlpatterns = [
    # course list/detail
    path('', views.CourseListView.as_view(), name='course_list'),
    path('subject/<slug:subject_slug>/', views.CourseListView.as_view(), name='course_list_subject'),
    path('detail/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('user/<str:username>/<int:pk>/', views.TeacherCourseListView.as_view(), name='teacher_courses'),
    # course edit
    path('create/', views.CreateCourseView.as_view(), name='course_create'),
    path('update/<int:pk>/', views.UpdateCourseView.as_view(), name='course_update'),
    path('delete/<int:pk>/', views.DeleteCourseView.as_view(), name='course_delete'),
    # course enroll
    path('enroll/', views.enroll, name='enroll'),
    # module
    path('<int:pk>/modules/', views.CourseModuleEditView.as_view(),
         name='course_module_update'),
    path('module/<int:pk>/content_list/', views.ModuleContentDetailView.as_view(),
         name='module_content_list'),
    # content_item
    path('module/<int:module_id>/content/<str:model_name>/create/', views.edit_module_content,
         name='module_content_create'),
    path('module/<int:module_id>/content/<str:model_name>/<int:id>/update/',
         views.edit_module_content, name='module_content_update'),
    path('content/<int:id>/delete/', views.delete_module_content, name='module_content_delete'),
    # group
    path('be_teacher/', views.be_teacher, name='be_teacher'),
]
