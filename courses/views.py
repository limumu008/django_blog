from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from courses.models import Course


class CourseListView(generic.ListView):
    template_name = 'courses/manage/course/list.html'
    context_object_name = 'courses'
    queryset = Course.objects.all()

    def get_queryset(self):
        try:
            user = get_user_model().objects.get(pk=self.kwargs['pk'])
            return Course.objects.filter(teacher=user)
        except KeyError:
            return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = get_user_model().objects.get(pk=self.kwargs['pk'])
            is_mine = True
        except KeyError:
            is_mine = False
        context['is_mine'] = is_mine
        return context


class CourseDetailView(generic.DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'courses/manage/course/detail.html'


class CreateCourseView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'courses.add_course'
    raise_exception = True
    permission_denied_message = "You haven't the permission."
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    template_name = 'courses/manage/course/create.html'

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class UpdateCourseView(PermissionRequiredMixin, generic.UpdateView):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    template_name = 'courses/manage/course/update.html'
    permission_required = 'courses.change_course'
    raise_exception = True


class DeleteCourseView(PermissionRequiredMixin, generic.DeleteView):
    model = Course
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('course:course_list')
    permission_required = 'courses.delete_course'
    raise_exception = True


def be_teacher(request):
    user = request.user
    user.profile.is_teacher = True
    user.save()
    # 添加 teacher group
    user.groups.add(3)
    messages.success(request, '成功成为老师')
    return redirect('account:profile')
