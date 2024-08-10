from domain.model import UserEntity
from django.contrib.auth import get_user_model
from .abstract_repository import AbstractRepository
from django.core.exceptions import FieldError
from django.contrib.auth import authenticate, login as auth_login

class DjangoUserRepository(AbstractRepository):
    def add(self, user: UserEntity):
        django_user = get_user_model()(username=user.username, email=user.email, first_name=user.first_name, last_name=user.last_name, patronymic=user.patronymic, password=user.password)
        django_user.save()

    def get(self, **kwargs) -> UserEntity:
        try:
            django_user = get_user_model().objects.filter(**kwargs).first()
        except FieldError:
            return None

        if not django_user:
            return None

        return UserEntity(
            username=django_user.username,
            email=django_user.email,
            first_name=django_user.first_name,
            last_name=django_user.last_name,
            patronymic=django_user.patronymic,
            password=django_user.password
        )
    
    def authenticate(self, user: UserEntity, request=None):
        django_user = authenticate(username=user.username, password=user.password)
        if django_user and request:
            auth_login(request, django_user)
        return django_user