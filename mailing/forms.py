from django import forms

from .models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "text_body"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "text_body": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
        }


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "recipients"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "message": forms.Select(attrs={"class": "form-control"}),
            "recipients": forms.SelectMultiple(attrs={"class": "form-control"}),
        }
