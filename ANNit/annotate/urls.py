from django.urls import path

from . import views

app_name = 'annotate'

urlpatterns = [
    path('', views.index, name='index'),
    path('load', views.load, name='load'),
    # ex: /polls/5/
    path('<int:entry_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:entry_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:entry_id>/decide/', views.decide, name='decide'),
    path('export', views.export, name='export'),
    path('<int:entry_id>/next_entry', views.next_entry, name='next_entry'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
