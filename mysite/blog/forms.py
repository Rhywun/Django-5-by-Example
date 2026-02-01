from django import forms


class EmailPostForm(forms.Form):
    fromName = forms.CharField(max_length=100)
    fromEmail = forms.EmailField()
    toEmail = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
