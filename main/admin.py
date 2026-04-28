from django.contrib import admin
from .models import Subject, Test, Question, TestResult, VideoLesson, Formula, Book

# Subject админ
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'icon']
    list_filter = ['grade']
    search_fields = ['name']

# VideoLesson админ (ВИДЕОСАБАҚТАР)
@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'duration', 'order']
    list_filter = ['subject']
    search_fields = ['title']
    ordering = ['order', 'subject']

# Formula админ (ФОРМУЛАЛАР)
@admin.register(Formula)
class FormulaAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject']
    list_filter = ['subject']
    search_fields = ['title']

# Question админ (Сұрақтар)
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3
    fields = ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct', 'points']

# Test админ (ТЕСТТЕР)
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'passing_score', 'time_limit']
    list_filter = ['subject']
    search_fields = ['title']
    inlines = [QuestionInline]

# TestResult админ (НӘТИЖЕЛЕР)
@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score', 'percentage', 'passed', 'completed_at']
    list_filter = ['test', 'passed']
    search_fields = ['user__username']

# Book админ (КІТАПХАНА)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'subject']
    list_filter = ['subject']
    search_fields = ['title']