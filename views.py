from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, send_mail
from django.utils.encoding import force_bytes, force_text
from tokens import account_activation_token
from forms import LoginForm, RegisterForm

from django.core.exceptions import ObjectDoesNotExist

def user_login(request):
	'''Вход пользователя в систему'''
	if request.method == 'POST' and request.POST:
		form = LoginForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data["name"]
			user_password = form.cleaned_data["password"]
			try:
				get_user = User.objects.get(username=user_name)
			except ObjectDoesNotExist:
				message = "Неверно введен логин или пароль."
				return render(request, 'login.html', {'form': form, 'message':message})
			if not get_user.is_active:
				return render(request, 'result_activation.html', {'answer':'В данный момент Вы являетесь неактивным членом форума. Для того, чтобы стать полноправным членом нашего дружного коллектива, подтвердите актуальность своей почты, перейдя по ссылке в отправленном вам письме. Спасибо, что Вы с нами.'})

			user = authenticate(username=get_user.username, password=request.POST["password"])
			if user.is_active:
				login(request, user)
				return redirect('/')
		else:
			message = "Ошибка ввода. Повторите попытку."
			return render(request, 'login.html', {'form': form, 'message':message})
	else:
		form = LoginForm()
		return render(request, 'login.html', {'form': form})

def sign_up(request):
	'''Регистрация пользователя'''
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data["user_name"]
			e_mail = form.cleaned_data["e_mail"]
			if form.cleaned_data["password1"] == form.cleaned_data["password2"]:
				password = form.cleaned_data["password1"]
				#создаём пользователя в базе данных, делаем его неактивным
				user = User.objects.create_user(username=user_name, email=e_mail, password=password)
				user.is_active = False
				user.save()
				#создаём письмо с активационной ссылкой
				current_site = get_current_site(request)
				mail_subject = 'Activate your account on site %s' % current_site
				message = render_to_string(
					'activate_message.html',
					{
					'user':user,
					'domain':current_site,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': account_activation_token.make_token(user)
					}
					)
				to_email = e_mail
				send_mail(
					mail_subject,
					message,
					'yuor@email',
					[to_email],
					html_message=message
					)
				return render(request, 'result_activation.html', {'answer': 'Please confirm your email address to comlete the registration.'}) 
	else:
		form = RegisterForm()
	return render(request, 'sign_up.html', {'form':form})

def activate_account(request, uidb64, token):
	''' Фукция обработки полученной ссылки активации'''
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		#делаем пользователя активным
		user.is_active = True
		user.save()
		#авторизация пользователя
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, user)
		return render(request, 'result_activation.html', {'answer':'Thanks for your confirm!'})
	else:
		return render(request, 'result_activation.html', {'answer':'Activate link is invalid!'})

def user_logout(request):
	'''Выход пользователя из системы'''
	logout(request)
	return redirect(request.META.get('HTTP_REFERER'))