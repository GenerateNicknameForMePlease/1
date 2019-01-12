from django.contrib import admin
from .models import Task, ResponseOnTask, Work_category


class Qqq(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('category',)}


class Treq(admin.ModelAdmin):
    fieldsets = [

        (None,               {'fields': ['responce_task', 'user_responce', 'intro_text_responce', 'responce_text']}),
    ]

    list_display = ('responce_task',)
    list_filter = ['user_responce']
    search_fields = ['intro_text_responce']


class Tre(admin.ModelAdmin):
    prepopulated_fields = {'slug1': ('intro_text', 'authors_name')}
    fieldsets = [

        (None,               {'fields': ['intro_text', 'task_text', 'authors_class', 'authors_name', 'end_date', 'slug1', 'status']}),
    ]

    list_display = ('intro_text',)
    list_filter = ['authors_name']
    search_fields = ['end_date']


admin.site.register(Work_category, Qqq)
admin.site.register(ResponseOnTask, Treq)
admin.site.register(Task, Tre)

