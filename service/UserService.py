from adapters.repository import UserEntity
from errors.UserErrors import UserAlreadyExists, InvalidPassword, UserDoesNotExists
from adapters import repository
from domain.helpers import hash_password_helper
import re

def register_user(username: str, email: str, first_name: str, last_name: str, patronymic: str, password: str):
    rep = repository.DjangoUserRepository()
    
    user = rep.get(email=email)
    if user:
        raise UserAlreadyExists(message='Пользователь с таким email уже существует')
    
    user = rep.get(username=username)
    if user:
        raise UserAlreadyExists(message='Пользователь с таким username уже существует')
    
    if not validate_password(password):
        raise InvalidPassword()

    user = UserEntity(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        password=hash_password_helper.hash_password(password)
    )

    try:
        rep.add(user)
    except:
        raise InvalidPassword()

    return UserEntity(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic
    )

def get_user(login: str, password: str):
    rep = repository.DjangoUserRepository()

    user = rep.get(email=login)
    if not user:
        user = rep.get(username=login)
        if not user:
            raise UserDoesNotExists()

    if hash_password_helper.check_password(password, user.password):
        return UserEntity(
            pk = user.pk,
            username = user.username,
            email = user.email,
            first_name = user.first_name,
            last_name = user.last_name,
            patronymic = user.patronymic
        )
    else:
        raise InvalidPassword()

def validate_password(password):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_-])[A-Za-z\d@$!#%*?&_-]{8,20}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    
    return mat