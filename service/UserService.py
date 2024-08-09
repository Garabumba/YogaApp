from adapters.repository import UserEntity
from errors.UserErrors import UserAlreadyExists, InvalidPassword
from adapters import repository
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
        password=password
    )

    try:
        rep.add(user)
    except:
        raise InvalidPassword()

    return user

def login(login: str, password: str):
    pass

def validate_password(password):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_-])[A-Za-z\d@$!#%*?&_-]{8,20}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    
    return mat