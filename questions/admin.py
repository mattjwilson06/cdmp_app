from django.contrib import admin

from .models import QuestionPool, Question, QuestionVersion, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Provides 4 empty answer forms by default

class QuestionVersionInline(admin.StackedInline):
    model = QuestionVersion
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    inlines = [QuestionVersionInline, AnswerInline]

@admin.register(QuestionPool)
class QuestionPoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')

admin.site.register(QuestionVersion)
admin.site.register(Answer)