from django import forms
from django.contrib.auth.models import User
from .models import ContactMessage, Subscriber
from django.contrib.auth.models import User
from .models import UserProfile, Product, Category

class ProfileImageForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    username = forms.CharField(max_length=150, required=True, label='Username')

    class Meta:
        model = UserProfile
        fields = ['profile_image', 'bio']  # UserProfile fields

    def __init__(self, *args, **kwargs):
        # Get the 'user' object passed through the form instance
        self.user = kwargs.pop('user', None)
        super(ProfileImageForm, self).__init__(*args, **kwargs)

        # Initialize the form fields with the user's existing data
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['username'].initial = self.user.username

    def save(self, commit=True):
        # Save the UserProfile data
        profile = super(ProfileImageForm, self).save(commit=False)
        if commit:
            profile.save()

        # Save the User data
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.username = self.cleaned_data['username']
            self.user.save()

        return profile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'category']


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'subject', 'email', 'phone', 'message']


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




