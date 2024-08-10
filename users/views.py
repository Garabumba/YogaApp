from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import get_user_model
import json
from service import UserService

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
            user = UserService.register_user(username, email, first_name, last_name, patronymic, password)
            django_user = get_user_model().objects.get(username=user.username)
            
            django_login(request, django_user)
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
            user = UserService.get_user(login, password)
            django_user = get_user_model().objects.get(username=user.username)
            
            django_login(request, django_user)
        except Exception as ex:
            return JsonResponse({'success': False, 'message': f'{ex}'}, status=400)

        return JsonResponse({'success': True}, status=200)
    
def me(request):
    if request.method == "GET":
        return JsonResponse({'name': request.user.first_name}, status=200)

@csrf_exempt
def logout(request):
    django_logout(request)