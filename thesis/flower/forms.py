# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.contrib.auth import (
    authenticate, get_user_model, )
from django.contrib.auth.models import User
from django.forms import *
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _


class CustomAuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = CharField(max_length=254)
    password = CharField(label=_(u"Parolă"), strip=False, widget=PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(
            UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(
                self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


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
        self.helper.layout = Layout(
            Fieldset(
                '',
                'nume',
                'prenume',
                'username',
                'parola',
                'email',
                'sex',
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
