from django import forms
from django.contrib import auth
from .models import Content, CellNo, Downloads
from django.contrib.auth import get_user_model


class ContentForm(forms.ModelForm):
        class Meta():
            model = Content
            fields =  {'type', 'category','keywords','filename'}
            widgets = {'downloaded': forms.HiddenInput(), 'usr': forms.HiddenInput()}
             
class NewUserForm(forms.ModelForm):
        class Meta():
            model = get_user_model()
            fields = {'username', 'password', 'email', 'first_name','last_name' }


class CellForm(forms.ModelForm):
        class Meta():
            model = CellNo
            fields = {'number'}
            widgets = {'usr': forms.HiddenInput()}

class DownloadForm(forms.ModelForm):
        class Meta():
            model = Downloads
            exclude = {'download_date'}
            widgets = {'content_id': forms.HiddenInput(), 'usr': forms.HiddenInput()}
