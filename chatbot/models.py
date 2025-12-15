from django.db import models

# Create your models here.


# ---------------------------------
# RAG / FAQ System
# ---------------------------------


class CommonQuestion(models.Model):
    question_text = models.TextField()
    answer_text = models.TextField()
    embedding = models.JSONField(null=True, blank=True)  # للتخزين الدلالي
    repeat_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text



class RawQuestion(models.Model):
    question_text = models.TextField()
    embedding = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text
