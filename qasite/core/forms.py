from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Answer  # <-- 关键的修改在这里，我们加入了 Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'bounty', 'image']

class SignUpForm(UserCreationForm):
    pass

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer # 现在，程序就认识 Answer 是什么了
        fields = ['content']