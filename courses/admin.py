from django.contrib import admin

from courses.models import Module, Course, Subject


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created', 'teacher']
    list_filter = ['created', 'subject', 'teacher']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Course, CourseAdmin)
