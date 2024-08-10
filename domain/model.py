from dataclasses import dataclass, field

@dataclass
class UserEntity:
    username: str
    email: str
    first_name: str
    last_name: str
    patronymic: str
    password: str = ''
    pk: int = 0