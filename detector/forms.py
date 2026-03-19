from django import forms

INPUT_CLASSES = 'w-full mt-1 rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900 bg-white p-2.5'

class EmailPostForm(forms.Form):
    email_sender = forms.EmailField(required=True, label="Sender's Email", widget=forms.TextInput(attrs={
            'placeholder': 'e.g., security@paypal-update.com',
            'class': INPUT_CLASSES
        }))
    email_text = forms.CharField(
    required=True,
    label="Email Body",
    widget=forms.Textarea(attrs={
            'rows': 5, 
            'placeholder': 'Paste the full body of the suspicious email here...',
            'class': INPUT_CLASSES
        }))