from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Subject, Course, Module, Content
from .serializers import SubjectSerializer, CourseSerializer, ModuleSerializer, ContentSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @action(detail=True, methods=['POST'])
    def enroll(self, request, pk=None):
        """ to enroll the course"""
        course = self.get_object()
        user = request.user
        if user not in course.students.all():
            course.students.add(user)
            enrolled = True
            return Response({'enrolled': enrolled})
        else:
            course.students.remove(user)
            enrolled = False
            return Response({'enrolled': enrolled})


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
