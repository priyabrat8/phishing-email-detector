from django import forms

class EmailPostForm(forms.Form):
    email_sender = forms.EmailField(required=True, label="Sender's Email")
    email_text = forms.CharField(
    required=True,
    label="Email Body",
    widget=forms.Textarea,)