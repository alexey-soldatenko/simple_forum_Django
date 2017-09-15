from django.shortcuts import render, redirect
from topics.models import Topics, TopicAnswers, Sections, Subsection
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def count_topic_answers(sect, subsect, page, num_topics_on_page):
	'''Функция подсчета ответов заданной темы'''
	page = int(page)
	#получаем список из тем, размещенных на одной странице (при помощи среза)
	topics = list(Topics.objects.filter(section_name= sect, subsection_name = subsect))[((page*num_topics_on_page) - num_topics_on_page): page*num_topics_on_page]
	count_answers = []
	for topic in topics:
		#помещаем в выходной список количество ответов к отдельной теме
		count_answers.append(TopicAnswers.objects.filter(topic_name=topic).count())
	return count_answers


# Create your views here.
def display_topics_in_subsection(request, sect, subsect, page=1):
	'''Функция отображения тем заданного подраздела'''

	section = Sections.objects.get(section_name = sect)
	subsection = Subsection.objects.get(subsection_name = subsect, section_name = section)
	topics = Topics.objects.filter(section_name = section, subsection_name = subsection)
	#количество тем на странице
	number_topics = 1
	paginator = Paginator(topics, number_topics)

	try:
		#все темы размещенные на конкретной странице page
		all_topics = paginator.page(page)
		#количество ответов для каждой из тем
		count_answers = count_topic_answers(section, subsection, page, number_topics)
	except PageNotAnInteger:
		all_topics = paginator.page(1)
		count_answers = count_topic_answers(section, subsection, 1, number_topics)
	except EmptyPage:
		all_topics = paginator.page(paginator.num_pages)
	return render(request, 'topics.html', {'all_topics':all_topics, 'count_answers':count_answers, 'number_topics_on_page': number_topics})


def display_topic(request, topic_id):
	'''Отображение на экране конкретной темы с ответами'''
	topic = Topics.objects.get(pk=topic_id)
	answers = TopicAnswers.objects.filter(topic_name = topic)
	return render(request, 'topic.html', {'topic':topic, 'answers':answers})



def save_answer(request, topic_id):
	'''Сохранение ответа в базе данных'''
	if request.method == 'POST':
		text = request.POST['answer']
		user_name = request.user.username
		date = datetime.now()
		try:
			topic_name = Topics.objects.get(pk=topic_id)
		except:
			return render(request, 'result_activation.html', {'answer':'Произошла ошибка!'})

		answer = TopicAnswers.objects.create(topic_name = topic_name, user_name = user_name, context = text, date = date)
		answer.save()
	else:
		pass
	#возвращение на страницу отправки запроса
	return redirect(request.META.get('HTTP_REFERER'))



def create_topic(request):
	'''Создание темы'''
	if request.user.is_anonymous():
		return render(request, 'result_activation.html', {'answer':'Создавать темы могут только зарегистрированные и автоматизированные пользователи!'})
	else:
		return render(request, 'create_topic.html')


def save_topic(request):
	'''Сохраниение созданной темы в базе данных '''

	#создавать темы могут лишь автоматизированные и активные пользователи
	if request.user.is_authenticated() and request.user.is_active:
		user_name = request.user.username 
		anonymous = False
		if request.method == 'POST' and request.POST:
			section = Sections.objects.get(section_name=request.POST["Section"])
			subsection = Subsection.objects.get(section_name=section, subsection_name=request.POST["Subsection"])
			title = request.POST["title"]
			context = request.POST["context"]
			date_time = datetime.now()
			#создание и сохранение темы, данные которой получены после их отправки POST-методом со страницы create_topic
			topic = Topics.objects.create(section_name=section, subsection_name=subsection, topic_name=title, author_name=user_name, context=context, date=date_time)
			topic.save()
			message = 'Тема успешно размещена!'
			return render(request, 'save_topic.html',{'message':message, 'anonymous': anonymous})
		else:
			message = 'Заполните все поля'
	else:
		message = 'Создавать темы могут только авторизированные пользователи!'
		anonymous = True
	return render(request, 'save_topic.html',{'message':message, 'anonymous': anonymous})

#домашняя страница	
def display_home(request):
	return render(request, 'home.html')


def display_profile(request):
	'''Отображение страницы профиля пользователя '''
	#получаем все темы пользователя и их количество
	topics = Topics.objects.filter(author_name=request.user.username)
	num_topics = Topics.objects.filter(author_name=request.user.username).count()
	#получаем все ответы пользователя и словарь, где ключ - это название темы, а значение - объект типа TopicAnswers, таким образом мы избавляемся от дублирования тем
	answers = TopicAnswers.objects.filter(user_name=request.user.username)
	out_answers = {}
	for answer in answers:
		out_answers[answer.topic_name] = answer
	num_answers = TopicAnswers.objects.filter(user_name=request.user.username).count()
	return render(request, 'profile.html', {'topics':topics, 'num_topics': num_topics, 'answers':out_answers, 'num_answers':num_answers})


def display_last_topics(request):
	'''Отображение последних 10 опубликованных тем '''
	topics = Topics.objects.all().order_by('-date')[:10]
	return render(request, 'last_topics.html', {'topics': topics})