from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    is_answered = forms.BooleanField()

    def clean_subject(self):
        data = self.cleaned_data["subject"]
        if "спасибо" not in data.lower():
            raise forms.ValidationError("Вы обязательно должны нас поблагодарить!")
        return data
