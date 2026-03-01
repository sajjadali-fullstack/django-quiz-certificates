from django.db import models
from django.contrib.auth.models import User




class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Difficulty(models.Model):
    level = models.CharField(max_length=50)  # e.g., Easy, Medium, Hard
    
    def __str__(self):
        return self.level

class Question(models.Model):
    text = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Quiz(models.Model):
    name = models.CharField(max_length=100,default='Java')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.name


class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total}"