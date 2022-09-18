from django.urls import path
from . import views

urlpatterns = [
    # path('', views.getData),
    path('trie', views.getTrie),
    path('index', views.getIndex),
    
]
