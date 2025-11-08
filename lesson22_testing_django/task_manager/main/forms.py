from django import forms
from datetime import date
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < date.today():
            raise forms.ValidationError("Дата виконання не може бути в минулому")
        return due_date