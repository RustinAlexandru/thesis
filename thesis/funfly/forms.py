# -*- coding: utf-8 -*-
import pytz
from allauth.account.forms import LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from funfly.models import PostComment


class CustomAuthenticationForm(AuthenticationForm):
    password = forms.CharField(label=_(u"Password"), strip=False, widget=forms.PasswordInput)

class CustomAuthenticationFormOauth(LoginForm):
    password = forms.CharField(label=_(u"Password"), strip=False, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        required=True,
    )

    last_name = forms.CharField(
        max_length=50,
        required=True,
    )

    username = forms.CharField(
        max_length=30,
        required=True,
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )

    email = forms.EmailField(
        widget=forms.EmailInput,
    )

    sex = forms.TypedChoiceField(
        label= u"Please select your gender!",
        choices=((1, "Male"), (0, "Female")),
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        initial='1',
        required=True,
    )

    city = forms.CharField(
        label='City',
        required=False,

    )

    timezone = forms.ChoiceField(
        label=_('Time Zone'),
        choices=[(t, t) for t in pytz.common_timezones]
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_register_form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-1'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'first_name',
                'last_name',
                'username',
                'password',
                'email',
                'sex',
                'city',
                'timezone',
            ),
            ButtonHolder(
                Submit('create', u'Create', css_class='button create')
                )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError(
                'Please choose another email, email already in use!')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).count():
            raise forms.ValidationError(
                'Username is already taken, pick another one!')
        return username


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['text']
        labels = {
            'text': _('Message'),
        }

        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Message...',
                                          'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_comment_form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2 col-md-2 col-sm-2'
        self.helper.field_class = 'col-lg-10 col-md-10 col-sm-10'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'text',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button submit')
            )
        )
