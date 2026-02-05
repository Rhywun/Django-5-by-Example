from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    your_name = forms.CharField(max_length=100)
    your_email = forms.EmailField()
    to_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentBoundField(forms.BoundField):
    """
    Wrap form fields in a `div` with the "comment" class.
    """

    comment_class = "comment"

    def css_classes(self, extra_classes=None) -> str:
        result = super().css_classes(extra_classes)
        if self.comment_class not in result:
            result += f" {self.comment_class}"
        return result.strip()


class CommentForm(forms.ModelForm):
    bound_field_class = CommentBoundField

    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
