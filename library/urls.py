"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from user import views as user_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('admin/', admin.site.urls),
	path('libtech/', include('libtech.urls')),

	path('register/', user_views.register, name='register'),
	path('login/', user_views.login_view, name='login'),
	path('logout/', user_views.logout_view, name='logout'),
	
	# path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
	path('profile/', user_views.profile, name='profile'),
	path('profile/update/', user_views.profile_update, name='profile-update'),

	path('passwordreset/',auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
	path('passwordresetdone/',auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
	path('passwordresetconfirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
	path('passwordresetcomplete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),

	# MOBILE
	#path('api/', include('reservation.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
