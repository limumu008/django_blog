from django.urls import reverse_lazy
from django.views import generic

from courses.models import Course


class CourseListView(generic.ListView):
    template_name = 'courses/manage/course/list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)


class CourseDetailView(generic.DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'courses/manage/course/detail.html'


class CreateCourseView(generic.CreateView):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    template_name = 'courses/manage/course/create.html'

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class UpdateCourseView(generic.UpdateView):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    template_name = 'courses/manage/course/update.html'


class DeleteCourseView(generic.DeleteView):
    model = Course
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('course:course_list')
