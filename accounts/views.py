from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings


class LogInView(LoginView):
    template_name = 'accounts/login.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, self.template_name)


class LogoutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'accounts/logout.html'
