from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        return comment