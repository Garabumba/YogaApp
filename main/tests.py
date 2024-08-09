from users.service import UserService, UnitOfWork
from users.errors.UserErrors import UserAlreadyExists, InvalidPassword, IncorrectLogin
from django.test import TestCase

from users.domain.model import UserEntity

class UserTestCase(TestCase):
    def test_register_user(self):
        self.assertEqual(UserService.register_user('test', 'test@mail.ru', 'test', 'test', 'test', 'testPassword1!'), 
                        UserEntity(
                            username='test',
                            email='test@mail.ru',
                            first_name='test',
                            last_name='test',
                            patronymic='test',
                            password='testPassword1!'
                        ))

        with self.assertRaises(UserAlreadyExists) as context:
            UserService.register_user(
                'test', 
                'test@mail.ru', 
                'test', 
                'test', 
                'test', 
                'testPassword1!'
            )
        self.assertEqual(str(context.exception), 'Пользователь с таким email уже существует')

        with self.assertRaises(InvalidPassword) as context:
            UserService.register_user(
                'test8', 
                'test8@mail.ru', 
                'test', 
                'test', 
                'test', 
                'testPassword'
            )
        self.assertEqual(str(context.exception), 'Некорректный пароль')

    def test_login_user(self):
        self.assertEqual(UserService.login('test', 'testPassword1!'),
                        UserEntity(
                        username='test',
                        email='test@mail.ru',
                        first_name='test',
                        last_name='test',
                        patronymic='test',
                        password='testPassword1!'
                    ))
        
        with self.assertRaises(IncorrectLogin) as context:
            UserService.login('tesst', 'testPassword1!')
        self.assertEqual(str(context.exception), 'Неверный логин или почта')

        with self.assertRaises(InvalidPassword) as context:
            UserService.login('test', 'testPassword1')
        self.assertEqual(str(context.exception), 'Неверный пароль')

class TestPasswordValidation(TestCase):
    def test_password_length(self):
        self.assertFalse(UserService.validate_password('Pwd1!'))
        self.assertFalse(UserService.validate_password('Pwd_1'))
        self.assertFalse(UserService.validate_password('Pass2'))
        self.assertTrue(UserService.validate_password('Password1!'))
        self.assertTrue(UserService.validate_password('Password_1'))
        self.assertFalse(UserService.validate_password('ThisIsARealVeryGoodPassword_100_percents'))

    def test_password_without_lower_symbols(self):
        self.assertFalse(UserService.validate_password('password1!'))
        self.assertFalse(UserService.validate_password('password_1'))
        self.assertFalse(UserService.validate_password('password_9090'))
        self.assertFalse(UserService.validate_password('123_pass_9090'))

    def test_password_without_upper_symbols(self):
        self.assertFalse(UserService.validate_password('PASSWORD1!'))
        self.assertFalse(UserService.validate_password('PASSWORD_1'))
        self.assertFalse(UserService.validate_password('VERYGOODPASS_1'))
        self.assertFalse(UserService.validate_password('1980_BIRTH_DATE!'))

    def test_password_without_special_symbols(self):
        self.assertFalse(UserService.validate_password('Password1'))
        self.assertFalse(UserService.validate_password('Password020799'))
        self.assertFalse(UserService.validate_password('koshkaMurka090385'))
        self.assertFalse(UserService.validate_password('crocodile920'))

    def test_password_without_numbers(self):
        self.assertFalse(UserService.validate_password('Password_first'))
        self.assertFalse(UserService.validate_password('Very_Good_Password'))
        self.assertFalse(UserService.validate_password('TwentyOne_!'))
        self.assertFalse(UserService.validate_password('Sunrise-second!'))

    def test_password_without_letters(self):
        self.assertFalse(UserService.validate_password('178232612!'))
        self.assertFalse(UserService.validate_password('921_218_2183@'))
        self.assertFalse(UserService.validate_password('1293-2121-!!!!'))
        self.assertFalse(UserService.validate_password('!75444&$&'))

    def test_passwords(self):
        self.assertTrue(UserService.validate_password('QwertY_1999'))
        self.assertTrue(UserService.validate_password('YhsaaQQ1!s@'))
        self.assertTrue(UserService.validate_password('ImIhor-1890'))
        self.assertTrue(UserService.validate_password('Anastasia99$'))
        self.assertTrue(UserService.validate_password('NikolaySmirnov@22'))
        self.assertTrue(UserService.validate_password('Lumpen_99'))
        self.assertTrue(UserService.validate_password('elepHant*78'))
        self.assertTrue(UserService.validate_password('11_LemoN_11'))
        self.assertTrue(UserService.validate_password('hsawww&22ASK'))
        self.assertFalse(UserService.validate_password('aSa22&'))
        self.assertFalse(UserService.validate_password('ysawwdsSujhgajhsjjjjsy@@www_22'))
        self.assertFalse(UserService.validate_password('innokentiy_2005'))
        self.assertFalse(UserService.validate_password('ALEKSANDR_2004'))
        self.assertFalse(UserService.validate_password('&&&&&&&_*'))
        self.assertFalse(UserService.validate_password('iskander'))
        self.assertFalse(UserService.validate_password('22011123621'))
        self.assertFalse(UserService.validate_password('20-02-20&20-02-21'))