from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from allauth.account.forms import SignupForm


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='RegisteredUsers')
        basic_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    # additional fields
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Firstname')
    last_name = forms.CharField(label='Lastname')

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2', )
