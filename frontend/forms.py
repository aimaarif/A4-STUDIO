from django import forms
from django.contrib.auth.models import User
from .models import ContactMessage, Subscriber
from django.contrib.auth.models import User
from .models import UserProfile, Product,  ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])
        }


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
        self.fields['username'].label = 'Username *'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Your Username'

        self.fields['first_name'].label = 'First Name'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'

        self.fields['last_name'].label = 'Last Name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'

        self.fields['email'].label = 'Email Adress *'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'

        self.fields['password'].label = 'Password *'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Your Password'




