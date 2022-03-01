from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm,UsernameField
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.translation import gettext,gettext_lazy as _
from .models import CustomUser
from django import forms
import re

UserModel = get_user_model()

mobile_pattern  = r'\b[0-9]{10}\b'
class CustomUserCreationForm(UserCreationForm):

    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    mobile=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Password Confirm',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    # auth_token = forms.CharField()
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if (re.fullmatch(mobile_pattern, mobile)):
            return mobile
        else:
            raise forms.ValidationError("Please Enter valid mobile number")
                

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','mobile','password1','password2')

class CustomUserEditForm(forms.Form):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    mobile=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    gender = forms.CharField(widget=forms.RadioSelect(attrs={'class':'form-control'}))
    dob = forms.CharField(widget=forms.DateInput(attrs={'class':'form-control'}))

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if (re.fullmatch(mobile_pattern, mobile)):
            return mobile
        else:
            raise forms.ValidationError("Please Enter valid mobile number")
              
    class Meta:
        model=CustomUser
        fields=('first_name','last_name','email','mobile','gender','dob')

class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        widgets = {
            'gender': forms.RadioSelect
        }
        exclude=('id',)
        # fields='__all__'

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')
 
    class Meta:
        model = CustomUser
        fields = ('email',)

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email Address',widget=forms.EmailInput(attrs={'class':'form-control form-control-sm'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))
    
    
class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('profile',) 

class UserAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control'}),
    )
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields['username'].max_length = username_max_length
        self.fields['username'].widget.attrs['maxlength'] = username_max_length
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)
    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
