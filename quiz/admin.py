from django.contrib import admin
from .models import Category, Quiz, Question


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "difficulty",
        "total_marks",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "quiz",
        "question",
        "correct_answer",
    )