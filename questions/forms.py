# questions/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import QuestionPool, Question, Answer, QuestionVersion

class QuestionPoolForm(forms.ModelForm):
    class Meta:
        model = QuestionPool
        fields = ['name']

class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)  

    class Meta:
        model = Question
        fields = ['name']  

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

class QuestionPoolSelectionForm(forms.Form):
    pools = forms.ModelMultipleChoiceField(
        queryset=QuestionPool.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

# We'll create the AnswerFormSet based on QuestionVersion instead of Question
AnswerFormSet = inlineformset_factory(
    QuestionVersion, 
    Answer, 
    form=AnswerForm, 
    extra=4, 
    can_delete=True,
    fields=['text', 'is_correct']
)