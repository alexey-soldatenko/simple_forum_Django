from django.contrib import admin
from topics.models import Sections, Subsection, Topics, TopicAnswers

class AdminTopics(admin.ModelAdmin):
	list_display = ['section_name', 'subsection_name', 'topic_name', 'author_name', 'date']

class AdminTopicAnswers(admin.ModelAdmin):
	list_dispaly = ['topic_name', 'user_name', 'date']

# Register your models here.
admin.site.register(Sections)
admin.site.register(Subsection)
admin.site.register(Topics, AdminTopics)
admin.site.register(TopicAnswers, AdminTopicAnswers)