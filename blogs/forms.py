from django import forms

from blogs.models import Comment


class PostCommentForm(forms.ModelForm):
    description = forms.CharField(label='Add a comment', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ['description']
