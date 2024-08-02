from django.db import models
from django.contrib.auth.models import User

class QuestionPool(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_pools')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_questions')
    created_at = models.DateTimeField(auto_now_add=True)
    current_version = models.ForeignKey('QuestionVersion', on_delete=models.SET_NULL, null=True, related_name='current_for')
    pools = models.ManyToManyField(QuestionPool, through='QuestionPoolAssociation')

    def __str__(self):
        return self.name

class QuestionPoolAssociation(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    pool = models.ForeignKey(QuestionPool, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['question', 'pool']

class QuestionVersion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='versions')
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_versions')
    created_at = models.DateTimeField(auto_now_add=True)
    version_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ['question', 'version_number']

    def __str__(self):
        return f"{self.question.name} - v{self.version_number}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    question_version = models.ForeignKey(QuestionVersion, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ['question', 'question_version', 'text']

    def __str__(self):
        return self.text
