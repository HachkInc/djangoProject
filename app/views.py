import os

from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app.utils import send_command


class SendCmdForm(forms.Form):
    ipField = forms.CharField(max_length=512, label='Адреса серверов', widget=forms.Textarea)
    cmdField = forms.CharField(max_length=512, label='Команда', widget=forms.Textarea)


@csrf_exempt
def my_view(request):
    if request.method == 'POST':
        form = SendCmdForm(request.POST)
        if form.is_valid():
            ips = form.cleaned_data['ipField'].split(",")
            ips = [ip.replace("\r\n", "") for ip in ips]
            cmd = form.cleaned_data['cmdField']
            res = send_command(hosts=ips, cmd=cmd)
            data = {"res": res, "ips": ips, "cmd": cmd}
            return render(request, template_name="output.html", context=data)
        else:
            form = SendCmdForm()
    else:
        form = SendCmdForm()
    return render(request, 'home.html', {'form': form})
