from .models import *
from typing import Any
from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,SetPasswordForm,UserChangeForm
from django.forms.widgets import  FileInput

User =get_user_model()

class SignupForm(UserCreationForm):
    #UserCreationForm Contains username,password1 and password2 fields
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label="Password(again)",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        #User model contains username,email,password,first_name,last_name fields
        fields=['email','name','phone']
        labels={
            'email':'Email',
        }
        error_messages={
            'email':{'required':'Email is required'}
        }
        widgets={
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'})
        }

class LoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__( *args,**kwargs)
        self.fields['username'].widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter email'})
        self.fields['password'].widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'})
    
    
class PassChangeForm(PasswordChangeForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['old_password'].widget=forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['new_password1'].widget=forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['new_password2'].widget=forms.PasswordInput(attrs={'class':'form-control'})

class PassSetForm(SetPasswordForm):
   def __init__(self,*args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['new_password1'].widget=forms.PasswordInput(attrs={'class':'form-control'})
       self.fields['new_password2'].widget=forms.PasswordInput(attrs={'class':'form-control'})

class EditUserProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=UserProfile
        fields='__all__'
        labels={
            'email':'Email'
        }
        
        widgets={
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'name':forms.EmailInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            
        }
class EditAdminProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields='__all__'
        

class MultipleFileInput(FileInput):
    def __init__(self,attrs=None, **kwargs):
        super().__init__(attrs=attrs,**kwargs)
        self.attrs.update({'multiple':True})

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'


class PostForm(forms.ModelForm):
     
    images = forms.ImageField(widget=MultipleFileInput, required=False)
    province = forms.ChoiceField(choices=Post.province_choices, label="Province", widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ['title', 'province', 'district', 'city', 'street', 'latitude','longitude','fare', 'description', 'identification_document', 'images']
        labels={
            'title':'Title'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2,'class':'form-control'}),
            'identification_document': forms.ClearableFileInput(attrs={'multiple': False}),
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'district':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'street':forms.TextInput(attrs={'class':'form-control'}),
            'latitude':forms.NumberInput(attrs={'class':'form-control'}),
            'longitude':forms.NumberInput(attrs={'class':'form-control'}),
            'fare':forms.TextInput(attrs={'class':'form-control'}),
        }
        


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        labels ={
            'comment':'Review',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2,'class':'form-control'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportPost
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 21,'cols':50,'class':'form-control'}),
        }