from django import forms


class submit_post(forms.Form):
    userid = forms.IntegerField(required=True)
    text = forms.CharField(widget=forms.Textarea)

class register(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget = forms.PasswordInput, required=True)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
