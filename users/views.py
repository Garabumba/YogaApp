from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from users.service import UserService

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username', '')
        email = data.get('email', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        patronymic = data.get('patronymic', '')
        password = data.get('password', '')

        try:
            result = UserService.register_user(username, email, first_name, last_name, patronymic, password)
        except Exception as ex:
            return JsonResponse({'success': False, 'message': f'{ex}'}, status=400)

        return JsonResponse({'success': True}, status=200)
    
    return JsonResponse({'success': False}, status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        login = data.get('login', '')
        password = data.get('password', '')

        try:
            result = UserService.login(login, password)
        except Exception as ex:
            return JsonResponse({'success': False, 'message': f'{ex}'}, status=400)

        return JsonResponse({'success': True}, status=200)