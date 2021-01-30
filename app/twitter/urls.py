from django.conf.urls import url
from .views import SearchResultView, HistoryView, HistoryListView


urlpatterns = [
    url(r'^search', SearchResultView.as_view()),
    url(r'^log', SearchResultView.as_view()),
    url(r'^history/(?P<id>\d+)$', HistoryView.as_view()),
    url(r'^history', HistoryListView.as_view()),
    
    ]