from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ("question_text", "grade")


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4
    fields = ("choice_text", "is_correct")


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text", "lesson", "grade")
    list_filter = ("lesson__course", "lesson")
    search_fields = ("question_text",)


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title", "content")
    ordering = ("course", "order")


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "pub_date", "total_enrollment")
    search_fields = ("name", "description")


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
