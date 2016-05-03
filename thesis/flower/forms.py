# -*- coding: utf-8 -*-
from allauth.account.forms import LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import *
from django.utils.translation import ugettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    password = CharField(label=_(u"Parolă"), strip=False, widget=PasswordInput)

class CustomAuthenticationFormOauth(LoginForm):
    password = CharField(label=_(u"Parolă"), strip=False, widget=PasswordInput)

class RegisterForm(Form):
    nume = CharField(
        max_length=50,
        required=True,
    )

    prenume = CharField(
        max_length=50,
        required=True,
    )

    username = CharField(
        max_length=30,
        required=True,
    )

    parola = CharField(
        label='Parolă',
        widget=PasswordInput,
    )

    email = EmailField(
        widget=EmailInput,
    )

    sexul = TypedChoiceField(
        label="Please select your gender",
        choices=((1, "Male"), (0, "Female")),
        coerce=lambda x: bool(int(x)),
        widget=RadioSelect,
        initial='1',
        required=True,
    )

    oras = CharField(
        label='Oraș',
        required=False,

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
                'nume',
                'prenume',
                'username',
                'parola',
                'email',
                'sexul',
                'oras',
            ),
            ButtonHolder(
                Submit('creeaza', u'Creează', css_class='button creeaza')
                )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise ValidationError(
                'Please choose another email, email already in use!')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).count():
            raise ValidationError(
                'Username is already taken, pick another one!')
        return username
