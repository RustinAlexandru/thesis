# -*- coding: utf-8 -*-
import pytz
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, HTML, Button
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from models import UserProfile
from django.utils.translation import ugettext_lazy as _

from funfly.models import PostComment
from PIL import Image as pil
import StringIO, time, os.path
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

class CustomAuthenticationForm(AuthenticationForm):
    password = forms.CharField(label=_(u"Password"), strip=False, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    def clean_remember_me(self):
        remember_me = self.cleaned_data['remember_me']
        if not remember_me:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
        else:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        return remember_me


# class CustomAuthenticationFormOauth(LoginForm):
#     password = forms.CharField(label=_(u"Password"), strip=False, widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    timezone = forms.ChoiceField(
        label=_('Time Zone'),
        choices=[(t, t) for t in pytz.common_timezones]
    )


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['sex', 'city', 'timezone', 'avatar']

        widgets = {
            'timezone': forms.Select(
                choices=[(t, t) for t in pytz.common_timezones])
        }

    def __init__(self, *args, **kwargs):
        # kwargs.pop('instance')
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_profile_edit_form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('sex', css_class='selectpicker'),
                'city',
                Field('timezone', css_class='selectpicker'),
                Field('avatar',  template='avatar_template.html'),
            ),
            ButtonHolder(
                Submit('update', u'Update', css_class='button create'),
                Button('cancel', 'Cancel', css_class='btn-default', onclick="window.history.back()")
            )
        )

    def resize_avatar(self):
        if hasattr(self.cleaned_data['avatar'], 'content_type'):

            img = pil.open(self.cleaned_data['avatar'])

            img.thumbnail((75, 75), pil.ANTIALIAS)

            thumb_io = StringIO.StringIO()
            img.save(thumb_io, self.cleaned_data['avatar'].content_type.split('/')[-1].upper())

            filename = self.cleaned_data['avatar'].name

            file = InMemoryUploadedFile(thumb_io,
                                        u"avatar",
                                        filename,
                                        self.files['avatar'].content_type,
                                        thumb_io.len,
                                        None)

            self.cleaned_data['avatar'] = file
            return self.cleaned_data['avatar']
        else:
            return self.cleaned_data['avatar']


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
        label=u"Please select your gender!",
        choices=((1, "Male"), (0, "Female")),
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        initial='1',
        required=False,
    )

    city = forms.CharField(
        label='City',
        required=False,

    )

    timezone = forms.ChoiceField(
        label=_('Time Zone'),
        choices=[(t, t) for t in pytz.common_timezones],
        required=False
    )

    avatar = forms.ImageField(
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_register_form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-5 col-md-5 col-sm-5 col-xs-5'
        self.helper.field_class = 'col-lg-6 col-md-6 col-sm-6 col-xs-6'
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
                Field('timezone', css_class='selectpicker'),
                'avatar',
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

    def resize_avatar(self):
        img = pil.open(self.cleaned_data['avatar'])

        img.thumbnail((75, 75), pil.ANTIALIAS)

        thumb_io = StringIO.StringIO()
        img.save(thumb_io, self.cleaned_data['avatar'].content_type.split('/')[-1].upper())

        filename = self.cleaned_data['avatar'].name

        file = InMemoryUploadedFile(thumb_io,
                                    u"avatar",
                                    filename,
                                    self.files['avatar'].content_type,
                                    thumb_io.len,
                                    None)

        self.cleaned_data['avatar'] = file
        return self.cleaned_data['avatar']


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


class AddItemForm(forms.Form):
    item_type = forms.ChoiceField(
        label=_('Please select which type of item you want to add'),
        choices=(('Ninegag', 'Ninegag'), ('Video', 'Video'), ('Joke', 'Joke'))
    )

    title = forms.CharField(max_length=200,
                            required=True)

    source_url = forms.CharField(max_length=200,
                                 required=False)

    media_file = forms.FileField(label='Please select a file to upload')

    text_area = forms.CharField(
        widget=forms.Textarea(),
    )

    def __init__(self, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_add_item_form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-6 col-md-6 col-sm-6'
        self.helper.field_class = 'col-lg-5 col-md-5 col-sm-5'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'item_type',
                'title',
                'source_url',
                'media_file',
                'text_area',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button submit')
            )
        )
