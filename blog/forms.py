from django import forms


class EmailArticleForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)
