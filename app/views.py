from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def my_view(request):
    if request.method == 'POST':
        # Обрабатываем отправленную форму
        form_data = request.POST
        field1 = form_data.get('field1')
        field2 = form_data.get('field2')
        # Делаем что-то с полями (например, сохраняем их в базу данных)
        return HttpResponse('Данные успешно отправлены!')
    else:
        # Выводим форму для заполнения с использованием Bootstrap
        return render(request, 'home.html')

