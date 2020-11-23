from django.urls import path

from . import views

app_name='learning_logs'


urlpatterns=[
        path('',views.index,name='index'),
        path('topics/',views.topics,name='topics'),
        path('topics/<int:topic_id>',views.topic,name='topic'),
        path('new_topics/',views.new_topic,name='new_topic'),
]

