from django.conf.urls import url
from .views import UserRegistrationView, UserLoginView


urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^signin', UserLoginView.as_view()),
    ]