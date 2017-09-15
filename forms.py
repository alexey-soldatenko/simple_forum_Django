from django import forms 

class LoginForm(forms.Form):
	name = forms.CharField(label="Ваше имя")
	password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")

class RegisterForm(forms.Form):
	user_name = forms.CharField(max_length=30, label='Ваше имя')
	e_mail = forms.EmailField(label='Эл. почта')
	password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
	password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')

