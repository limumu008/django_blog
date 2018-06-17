from rest_framework import routers

from .views import SubjectViewSet, CourseViewSet, ModuleViewSet, ContentViewSet

course_router = routers.DefaultRouter()
course_router.register(r'subjects', SubjectViewSet)
course_router.register(r'courses', CourseViewSet)
course_router.register(r'modules', ModuleViewSet)
course_router.register(r'contents', ContentViewSet)
