from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:entry_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:entry_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:entry_id>/decide/', views.decide, name='decide'),
]
