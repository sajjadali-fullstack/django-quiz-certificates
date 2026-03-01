from django import forms
from .models import Question,Choice

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)

        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                label=question.text,
                queryset=question.choices.all(),
                widget=forms.RadioSelect,
                empty_label="No Anshwer",
                required=False
                )




from .models import Category, Difficulty

class QuizFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    difficulty = forms.ModelChoiceField(queryset=Difficulty.objects.all(), required=True)
    widget=forms.Select(attrs={'class': 'form-select'})


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", 'first_name','last_name']