from django.conf.urls import include, url


urlpatterns = [
		url(r'(?P<sect>(C|C_plus_plus|Python|Databases|other))/(?P<subsect>[\x20-\x7E]+)/(?P<page>\d{1,2})?', 'topics.views.display_topics_in_subsection'),

]