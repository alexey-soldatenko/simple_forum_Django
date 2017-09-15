from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'simple_forum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'topics.views.display_home'),
    url(r'^create_topic$', 'topics.views.create_topic'),
    url(r'^save_topic', 'topics.views.save_topic'),
    url(r'^login$', 'views.user_login'),
    url(r'^sign_up$','views.sign_up'),
    url(r'^logout$', 'views.user_logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'views.activate_account', name='activate'),
    url(r'^topics/', include('topics.urls')),
    url(r'^topic/(?P<topic_id>\d+)$', 'topics.views.display_topic'),
    url(r'^save_answer/(?P<topic_id>\d+)$', 'topics.views.save_answer'),
    url(r'my_profile', 'topics.views.display_profile'),
    url(r'last_topics', 'topics.views.display_last_topics'),
]
