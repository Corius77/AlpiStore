from django import forms

class MessageForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    topic = forms.CharField(label="topic", max_length=200)
    email = forms.CharField(label="Email", max_length=200)
    message = forms.CharField(label="Message", max_length=200, widget=forms.Textarea)