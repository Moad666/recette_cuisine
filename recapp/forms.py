from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm,PasswordResetForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from .models import Recette

class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)






    
    
