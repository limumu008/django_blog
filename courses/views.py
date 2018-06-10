import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import ModuleFormSet
from .models import Course, Module, Content, Subject
from .utils import get_model, get_modelform


class CourseListView(generic.ListView):
    model = Course
    template_name = 'courses/course/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))
        try:
            subject_slug = self.kwargs.get('subject_slug')
            subject = get_object_or_404(Subject, slug=subject_slug)
            courses = Course.objects.filter(subject=subject)
        except Exception as e:
            subject = None
        context = super().get_context_data(**kwargs)
        context['subjects'] = subjects
        context['courses'] = courses
        context['subject'] = subject
        return context


class TeacherCourseListView(generic.ListView):
    template_name = 'courses/manage/course/list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        user = get_user_model().objects.get(pk=self.kwargs['pk'])
        return Course.objects.filter(teacher=user)


class StudentCourseListView(LoginRequiredMixin, generic.ListView):
    template_name = 'courses/students/course/list.html'
    context_object_name = 'student_courses'

    def get_queryset(self):
        courses = Course.objects.filter(students=self.request.user)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        course = context['course']
        if user.is_authenticated:
            is_logined = True
            if course not in user.courses_joined.all():
                is_enrolled = False
            else:
                is_enrolled = True
        else:
            is_logined = False
            is_enrolled = False
        context['is_logined'] = is_logined
        context['is_enrolled'] = is_enrolled
        return context


class StudentCourseDetailView(generic.DetailView):
    """ 实际是 Module 的类图，名字不重要"""
    model = Module
    template_name = 'courses/students/course/detail.html'
    context_object_name = 'module'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        course = self.object.course
        context['course'] = course
        return context


class CreateCourseView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'courses.add_course'
    raise_exception = True
    permission_denied_message = "You haven't the permission."
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    template_name = 'courses/manage/course/create.html'

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        self.object = form.save()
        Module.objects.create(course=self.object, title='')
        return super().form_valid(form)

    def get_success_url(self):
        module = self.object.modules.first()
        return module.get_absolute_url()


class UpdateCourseView(PermissionRequiredMixin, generic.UpdateView):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    template_name = 'courses/manage/course/update.html'
    permission_required = 'courses.change_course'
    raise_exception = True

    def get_success_url(self):
        module = self.object.modules.first()
        return module.get_absolute_url()


class DeleteCourseView(PermissionRequiredMixin, generic.DeleteView):
    model = Course
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('course:course_list')
    permission_required = 'courses.delete_course'
    raise_exception = True


class ModuleContentDetailView(generic.DetailView):
    model = Module
    template_name = 'courses/manage/module/content_list.html'
    context_object_name = 'module'


class CourseModuleEditView(generic.UpdateView):
    context_object_name = 'course'
    template_name = 'courses/manage/module/formset.html'

    def get_object(self, queryset=None):
        """ get the course will be edited"""
        return Course.objects.get(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        if self.request.method == 'POST':
            formset = self.get_formset(data=self.request.POST)
        else:
            formset = self.get_formset()
        kwargs['formset'] = formset
        kwargs['course'] = self.get_object()
        return kwargs

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.get_object(), data=data)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            module = Course.objects.get(pk=self.kwargs.get('pk')).modules.first()
            return redirect(module)


def edit_module_content(request, module_id, model_name, *, id=None):
    module = get_object_or_404(Module, pk=module_id)
    model = get_model(model_name)
    # 获取创建 content 类型的 model,用于创建 ModelForm
    if id:
        # 提供 id，update
        content_object = get_object_or_404(model, pk=id, owner=request.user)
    else:
        # 不提供 id，create
        content_object = None
    if request.method == 'POST':
        form = get_modelform(model)(data=request.POST, files=request.FILES, instance=content_object)
        if form.is_valid():
            content_object = form.save(commit=False)
            content_object.owner = request.user
            content_object.save()
            if not id:
                Content.objects.create(module=module, target=content_object)
            return redirect(module)
    else:
        form = get_modelform(model)(instance=content_object)
    context = {'form': form, 'object': content_object}
    return render(request, 'courses/manage/module/form.html', context)


def delete_module_content(request, id):
    if request.method == 'POST':
        content = get_object_or_404(Content, id=id, module__course__teacher=request.user)
        module = content.module
        content.target.delete()
        content.delete()
        return redirect(module)


def be_teacher(request):
    """ get group teacher"""
    user = request.user
    user.profile.is_teacher = True
    user.save()
    # 添加 teacher group
    user.groups.add(3)
    messages.success(request, '成功成为老师')
    return redirect('account:profile')


def enroll(request):
    """user enroll course"""
    user = request.user
    is_enrolled = json.loads(request.POST.get('is_enrolled'))
    course_id = json.loads(request.POST.get('course_id'))
    if not is_enrolled:
        user.courses_joined.add(course_id)
    else:
        user.courses_joined.remove(course_id)
    is_enrolled = not is_enrolled
    return JsonResponse({'is_enrolled': is_enrolled})
