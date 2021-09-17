

from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from django.conf.urls.static import static
from django.conf import settings

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/",include('api.urls')),
    path("",views.Home,name='home'),  
    path("loginPage/",views.LoginPage,name='loginpage'),
    path("registerPage/",views.RegisterPage,name='registerpage'),

] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
