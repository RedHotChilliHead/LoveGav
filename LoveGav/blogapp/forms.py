from django.forms import ModelForm

from blogapp.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]