class UserAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
    
class InvalidPassword(Exception):
    def __init__(self):
        super().__init__()
        self.message = 'Некорректный пароль'

    def __str__(self):
        return self.message

class IncorrectLogin(Exception):
    def __init__(self):
        super().__init__()
        self.message = 'Неверный логин или почта'

    def __str__(self):
        return self.message