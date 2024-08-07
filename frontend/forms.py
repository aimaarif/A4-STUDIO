from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = '<br><span class="form-text text-muted"><small>Allowed Letters, digits, @/./+/-/_ and max char 150 .</small></span>'
        self.fields['username'].widget.attrs['label'] = '<h5>Username</h5>'

        self.fields['first_name'].widget.attrs['label'] = '<h5>First Name</h5>'

        self.fields['last_name'].widget.attrs['label'] = '<h5>Last Name</h5>'

        self.fields['email'].widget.attrs['label'] = '<h5>Email Adress</h5>'

        self.fields['password'].widget.attrs['label'] = '<h5>Password</h5>'




