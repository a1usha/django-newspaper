from django import forms
from django.contrib.auth.models import User, Group
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


# ModelForm allows to create form that will work sith 
# specific database model
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class UserForm(UserCreationForm):
    # group = forms.Select(choices=[
    #     ('simple_user', 'Simple user'),
    #     ('copy_editor', 'Copy editor')
    # ])

    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('username', 'group', 'password1' ,'password2' )