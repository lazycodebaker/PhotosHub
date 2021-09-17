
from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path("register/",views.Register,name='register'),
    path("verify/<slug:auth_token>",views.verify,name='verify'),
    path("login/",views.Login,name='login'),
    path("logout/",views.Logout,name='logout'),
    path("upload/",views.Upload,name='upload'),
    url(r"^register/verify/$",views.VerifyPage,name='verifypage'),
]
