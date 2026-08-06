from django.core.exceptions import ValidationError
from django import forms
from .models import Account

class RegisterationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm Password",
            'class': 'form-control'
        })
    )


    
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "phone_number", "password"]

    # common CSS for all field
    def __init__(self, *args, **kwargs):
        super(RegisterationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs['placeholder'] = "Enter First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter Last Name"
        self.fields['email'].widget.attrs["placeholder"] = "Enter Your Email"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Enter Your Phone Number"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(RegisterationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(
                "Password does not match",
                code="password_does_not_match"
            )