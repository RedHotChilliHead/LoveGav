from django.forms import ModelForm

from blogapp.models import Comment


class CommentForm(ModelForm):
    """
    Форма ввода текста комментария к посту
    """
    class Meta:
        model = Comment
        fields = ["body"]