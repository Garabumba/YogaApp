import abc

from django.forms import ValidationError
from users.domain.model import UserEntity
from django.contrib.auth import get_user_model
#from django.contrib.auth.password_validation import validate_password

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, user: UserEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, email: str) -> UserEntity:
        raise NotImplementedError
    
class DjangoUserRepository(AbstractRepository):
    def add(self, user: UserEntity):
        #validate_password(user.password)

        django_user = get_user_model()(username=user.username, email=user.email, first_name=user.first_name, last_name=user.last_name, patronymic=user.patronymic, password=user.password)
        django_user.set_password(user.password)
        django_user.save()

    def get(self, **kwargs) -> UserEntity:
        django_user = get_user_model().objects.filter(**kwargs).first()

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