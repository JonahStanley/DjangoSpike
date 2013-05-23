from django import forms

class submit_post(forms.Form):
    userid = forms.IntegerField(required=True)
    text = forms.CharField(widget=forms.Textarea)