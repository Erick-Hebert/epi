
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
   
    #
    path('', RedirectView.as_view(url='auth/')),
    # Direciona para páginas do nucleo (site)
    path('home/', include('nucleo.urls')),
    path('auth/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'), 
    # Direciona para páginas nativas do django, login e logout
    path('auth/', include('django.contrib.auth.urls'), name="auth"),
    path('admin/', admin.site.urls),
]
