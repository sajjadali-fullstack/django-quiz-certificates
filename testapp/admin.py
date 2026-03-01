from django.contrib import admin
from testapp.models import Question,Choice,Category,Difficulty,Quiz
# Register your models here.





admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Category)
admin.site.register(Difficulty)
admin.site.register(Quiz)

