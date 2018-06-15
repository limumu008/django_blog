from rest_framework import serializers

from courses.models import Subject, Course, Module, Content


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ('url', 'title', 'slug')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.username')

    class Meta:
        model = Course
        # fields can include foreignkey related name.
        fields = ('url', 'subject', 'title', 'slug', 'overview',
                  'created', 'modules', 'teacher')


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module
        fields = ('url', 'course', 'title', 'description')


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    target = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ('order', 'target', 'module')
