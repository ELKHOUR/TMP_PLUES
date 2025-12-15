from django.contrib import admin
from .models import CommonQuestion, RawQuestion

# Register your models here.
@admin.register(CommonQuestion)
class CommonQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "repeat_count", "created_at")
    ordering = ("-repeat_count",)
    search_fields = ("question_text",)

@admin.register(RawQuestion)
class RawQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "count", "answered", "created_at")
    ordering = ("-count",)
    search_fields = ("question_text",)