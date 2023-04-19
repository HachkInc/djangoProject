import os

from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.utils import send_command
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages


class SendCmdForm(forms.Form):
    ipField = forms.CharField(max_length=512, label='Адреса серверов', widget=forms.Textarea)
    cmdField = forms.CharField(max_length=512, label='Команда', widget=forms.Textarea)


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('send')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

@login_required
@csrf_exempt
def my_view(request):
    if request.method == 'POST':
        form = SendCmdForm(request.POST)
        if form.is_valid():
            ips = form.cleaned_data['ipField'].split(",")
            ips = [ip.replace("\r\n", "") for ip in ips]
            ips = [ip.replace(" ", "") for ip in ips]
            cmd = form.cleaned_data['cmdField']
            res = {}
            for ip in ips:
                res[ip] = send_command(host=ip, cmd=cmd)
            data = {"res": res, "ips": ips, "cmd": cmd}
            return render(request, template_name="output.html", context=data)
        else:
            form = SendCmdForm()
    else:
        form = SendCmdForm()

    return render(request, 'home.html', {'form': form})
