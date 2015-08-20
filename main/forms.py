from django import forms
from django.core.validators import RegexValidator
from main.models import Division, Board, Comment

letter_validator = RegexValidator(r'^[a-zA-Z]*$','Please Type Letters')

class DivisionForm(forms.ModelForm):
	class Meta:
		model = Division
		fields = ['name',]

class BoardForm(forms.ModelForm):
	class Meta:
		model = Board
		fields = ['name',]

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['text',]



class UserSignup(forms.Form):
	name = forms.CharField(required=True, validators=[letter_validator])
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput(), required=True)

class UserLogin(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())

