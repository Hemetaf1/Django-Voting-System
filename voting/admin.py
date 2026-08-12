from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project
from .models import Section, Project, Vote, Feedback



@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'order')
    list_editable = ('slug', 'order')
    prepopulated_fields = {'slug': ('name',)}   # وقتی نام را تایپ می‌کنید، اسلاگ خودکار ساخته شود
    list_filter = ('category',)
    ordering = ('category','order')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'slug')
    list_editable = ('slug',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('section__category',)
    search_fields = ('title',)

admin.site.register(Vote)
admin.site.register(Feedback)
