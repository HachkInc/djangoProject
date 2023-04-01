from django import forms
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


class SendCmdForm(forms.Form):
    ipField = forms.CharField(max_length=512)
    cmdField = forms.CharField(max_length=512, label='Команда')


@csrf_exempt
def my_view(request):
    if request.method == 'POST':
        form = SendCmdForm(request.POST)
        if form.is_valid():
            ips = form.cleaned_data['ipField'].split()
            cmd = form.cleaned_data['cmdField']
            return HttpResponse(f"ips: <p>{ips}</p> <p>cmd {cmd}</p>")
        else:
            form = SendCmdForm()
    else:
        form = SendCmdForm()
    return render(request, 'home.html', {'form': form})
