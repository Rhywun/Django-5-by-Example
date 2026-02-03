from django import forms


class EmailPostForm(forms.Form):
    your_name = forms.CharField(max_length=100)
    your_email = forms.EmailField()
    to_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
