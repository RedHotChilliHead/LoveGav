import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from profileapp.models import Profile, Pet


# c = Client()
# get(path, data=None, follow=False, secure=False, *, headers=None, **extra)
# with open("wishlist.doc", "rb") as fp:
# ...     c.post("/customers/wishes/", {"name": "fred", "attachment": fp})
# head(path, data=None, follow=False, secure=False, *, headers=None, **extra)
# options(path, data='', content_type='application/octet-stream', follow=False, secure=False, *, headers=None, **extra)
# put(path, data='', content_type='application/octet-stream', follow=False, secure=False, *, headers=None, **extra)
# patch(path, data='', content_type='application/octet-stream', follow=False, secure=False, *, headers=None, **extra)
# delete(path, data='', content_type='application/octet-stream', follow=False, secure=False, *, headers=None, **extra)
# c.login(username="fred", password="secret") logout()
#         if response.status_code == 200:
#             form_errors = response.context['form'].errors
#             print("Form errors:", form_errors)

class UserAndProfileRegisterTestCase(TestCase):
    """
    Проверка того, что view register правильно создает пользователя и профиль
    """

    def test_user_registration_view(self):
        username = 'testuser'
        password = 'testpassword'
        post_data = {
            'username': username,
            'password1': password,
            'password2': password,
        }
        response = self.client.post(reverse('profileapp:register'), post_data)

        # Убеждаемся, что ответ является перенаправлением (успешная отправка формы)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=username).exists())

        self.assertTrue(User.objects.filter(username=username).exists())  # Убеждаемся, что пользователь создан

        user = User.objects.get(username=username)  # Убеждаемся, что профиль создан
        self.assertTrue(Profile.objects.filter(user=user).exists())

        # Проверяем, что пользователь перенаправлен на страницу его профиля
        response = self.client.get(reverse('profileapp:user-details', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)

        self.assertTrue(user.is_authenticated)  # Проверяем, что пользователь авторизован


class UserLoginLogoutTestCase(TestCase):
    """
    Проверка входа по логину и паролю и выхода из аккаунта пользователя
    """

    @classmethod
    def setUpClass(cls):
        cls.username = "testuser"
        cls.password = "testpassword"
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)
        cls.user.profile = Profile.objects.create(user=cls.user, bio="It is a test")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_user_login_view(self):
        response = self.client.post(reverse('profileapp:login'), {"username": self.username, "password": self.password},
                                    format='json')
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create a post', html=True)

    def test_user_logout_view(self):
        response = self.client.get(reverse('profileapp:logout'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login', html=True)


class UserAndProfileTestCase(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.profile = Profile.objects.create(user=self.user, bio="It is a test")
        self.client.login(username=self.username, password=self.password)

    def tearDown(self) -> None:
        self.user.delete()

    def test_user_detail_view(self):
        """
        Проверка корректного отображения приватного профиля пользователя через user-details
        """
        response = self.client.get(reverse('profileapp:user-details', kwargs={"username": self.username}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bio: It is a test')

    def test_user_update_view(self):
        """
        Проверка корректного обновления профиля пользователя через update-me
        """
        response = self.client.post(reverse('profileapp:update-me', kwargs={"username": self.username}),
                                    {"bio": "Updated bio",
                                     "email": "cucumber@cucumber.com"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profileapp:user-details', kwargs={"username": self.username}))
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Updated bio')
        self.assertContains(response, 'Email: cucumber@cucumber.com', html=True)

    def test_user_deletion_view(self):
        """
        Проверка того, что delete-me правильно выполняет удаление пользователя и профиля
        """
        # Получаем страницу подтверждения удаления
        response = self.client.get(
            reverse('profileapp:delete-me', kwargs={'username': self.user.username, 'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)  # Ожидаем код 200, так как это страница подтверждения

        # Отправляем запрос для подтверждения удаления
        response = self.client.post(
            reverse('profileapp:delete-me', kwargs={'username': self.user.username, 'pk': self.user.pk}))
        self.assertRedirects(response, reverse('blogapp:posts-list'))  # Ожидаем перенаправление на домашнюю страницу

        # Проверка, что пользователь и профиль удалены
        self.assertFalse(User.objects.filter(username=self.user.username).exists())
        self.assertFalse(Profile.objects.filter(user=self.user).exists())


class APIUserAndProfileTestCase(TestCase):
    def setUp(self):
        self.username = "testuser5"
        self.password = "testpassword1235"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.profile = Profile.objects.create(user=self.user, bio="It is a test", birth="1996-10-03")
        # self.client.login(username=self.username, password=self.password)

    def tearDown(self) -> None:
        self.user.delete()

    def test_user_registration_api_view(self):
        """
        Проверка того, что api-users правильно создает пользователя и профиль
        """
        username = "testuser1"
        password = "testpassword1"
        post_data = {
            "username": username,
            "password": password,
            "profile": {
                "bio": "It is a test",
                "email": "test@test.com",
                "birth": "1995-10-03"
            }
        }
        post_data_json = json.dumps(post_data)  # для того, что бы Python передал данные не как словарь, а как json

        response = self.client.post(reverse('profileapp:api-users'), post_data_json, content_type='application/json')

        self.assertEqual(response.status_code, 201)  # Убеждаемся, что ответ является Created (успешное создание)

        self.assertTrue(User.objects.filter(username=username).exists())  # Убеждаемся, что пользователь создан

        # Убеждаемся, что профиль создан
        user = User.objects.get(username=username)
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertTrue(user.is_authenticated)  # Проверяем, что пользователь авторизован

    def test_user_list_api_view(self):
        """
        Проверка просмотра списка всех пользователей через api-users
        """
        response = self.client.get(reverse('profileapp:api-users'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser5")
        self.assertContains(response, "It is a test")

    def test_user_update_api_view(self):
        """
        Проверка обновления данных пользователя через api-user-details
        """
        post_data = {
            "username": "testuser5",
            "profile": {
                "bio": "Updated bio",
                "email": "cucumber@cucumber.com"
            }
        }
        post_data_json = json.dumps(post_data)  # для того, что бы Python передал данные не как словарь, а как json
        response = self.client.post(reverse('profileapp:api-user-details', kwargs={'pk': self.user.pk}), post_data_json,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Updated bio')
        self.assertEqual(self.user.profile.email, 'cucumber@cucumber.com')

    def test_user_detail_api_view(self):
        """
        Проверка отображения детальной информации о пользователе с помощью api-user-details
        """
        response = self.client.get(reverse('profileapp:api-user-details', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)

        expected_data = {
            'pk': self.user.pk,
            'username': 'testuser5',
            'profile': {
                'bio': 'It is a test',
                'email': '',
                'birth': '1996-10-03'
            }
        }

        # Преобразуем контент ответа в словарь
        response_data = json.loads(response.content)

        self.assertEqual(response_data, expected_data)

    def test_user_delete_api_view(self):
        """
        Проверка удаления пользователя с помощью api-user-details
        """
        username = "testuser0"
        password = "testpassword0"
        user = User.objects.create_user(username=username, password=password)
        user.profile = Profile.objects.create(user=user, bio="0")
        response = self.client.delete(reverse('profileapp:api-user-details', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(username=username).exists())
        self.assertFalse(Profile.objects.filter(user=user).exists())


class PetProfileTestCase(TestCase):
    create_data = {
        "name": "Marusya",
        "sex": "F",
        "specie": "Dog",
        "breed": "Spitz",
        "color": "Red",
    }

    def setUp(self):
        self.username = "testuser5"
        self.password = "testpassword1235"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.profile = Profile.objects.create(user=self.user, bio="It is a test", birth="1996-10-03")
        self.client.login(username=self.username, password=self.password)
        self.pet = Pet.objects.create(name=PetProfileTestCase.create_data['name'],
                                      sex=PetProfileTestCase.create_data['sex'],
                                      specie=PetProfileTestCase.create_data['specie'],
                                      breed=PetProfileTestCase.create_data['breed'],
                                      color=PetProfileTestCase.create_data['color'],
                                      owner=self.user)

    def tearDown(self) -> None:
        self.user.delete()

    def test_pet_register_view(self):
        """
        Проверка создания странички питомца через register-pet
        """
        post_data = {
            "name": "Sharik",
            "sex": "M",
            "specie": "Dog",
            "breed": "Mongrel",
            "color": "Grey",
            "birth": "2014-08-07",
            "chip": False,
            "tatoo": "",
            "date_tatoo": "",
            "passport": "",
            "weight": 10
        }

        response = self.client.post(reverse("profileapp:register-pet", kwargs={"username": self.username}), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profileapp:user-details', kwargs={"username": self.username}))
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sharik")
        self.assertTrue(Pet.objects.filter(owner=self.user, name=post_data['name']).exists())

    def test_pet_details_view(self):
        """
        Проверка детального отображения информации о питомце через pet-details
        """
        response = self.client.get(
            reverse('profileapp:pet-details', kwargs={"username": self.username, "pk": self.pet.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, PetProfileTestCase.create_data['name'])
        self.assertContains(response, PetProfileTestCase.create_data['breed'])
        self.assertContains(response, PetProfileTestCase.create_data['color'])

    def test_pet_update_view(self):
        """
        Проверка обновления информации о питомце через update-pet
        """
        weight = 5.0
        response = self.client.post(
            reverse("profileapp:update-pet", kwargs={"username": self.username, "pk": self.pet.pk}),
            {'weight': weight})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('profileapp:pet-details', kwargs={"username": self.username, "pk": self.pet.pk}))
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        print(response.content)
        self.user.profile.refresh_from_db()
        pet = Pet.objects.get(pk=self.pet.pk)
        self.assertEqual(pet.weight, weight)
        self.assertContains(response, f'Weight: {weight} (kg)', html=True)

    def test_pet_delete_view(self):
        """
        Проверка удаления профиля питомца через delete-pet
        """
        response = self.client.get(
            reverse('profileapp:delete-pet', kwargs={'username': self.user.username, "pk": self.pet.pk}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('profileapp:delete-pet', kwargs={'username': self.user.username, 'pk': self.pet.pk}))
        self.assertRedirects(response, reverse('profileapp:user-details', kwargs={'username': self.user.username}))

        self.assertFalse(Pet.objects.filter(name=self.create_data['name'], owner=self.user).exists())


class APIPetTestCase(TestCase):
    create_data = {
        "name": "Marusya",
        "sex": "F",
        "specie": "Dog",
        "breed": "Spitz",
        "color": "Red",
    }

    def setUp(self):
        self.username = "testuser5"
        self.password = "testpassword1235"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.profile = Profile.objects.create(user=self.user, bio="It is a test", birth="1996-10-03")
        self.client.login(username=self.username, password=self.password)
        self.pet = Pet.objects.create(name=PetProfileTestCase.create_data['name'],
                                      sex=PetProfileTestCase.create_data['sex'],
                                      specie=PetProfileTestCase.create_data['specie'],
                                      breed=PetProfileTestCase.create_data['breed'],
                                      color=PetProfileTestCase.create_data['color'],
                                      owner=self.user)

    def tearDown(self) -> None:
        self.user.delete()

    def test_pet_registration_api_view(self):
        """
        Проверка того, что api-users правильно создает профиль питомца
        """
        post_data = {
            "name": "SharikAPI",
            "sex": "M",
            "specie": "Dog",
            "breed": "Mongrel",
            "color": "Grey",
            "birth": "2021-08-07",
            "weight": 10
        }

        post_data_json = json.dumps(post_data)

        response = self.client.post(reverse('profileapp:pet-list'), post_data_json, content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Убеждаемся, что ответ является Created (успешное создание)
        self.assertTrue(Pet.objects.filter(name=post_data['name'], owner=self.user).exists())

    def test_user_list_api_view(self):
        """
        Проверка просмотра списка питомцев через api-users
        """
        response = self.client.get(reverse('profileapp:pet-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, PetProfileTestCase.create_data['name'])

    def test_user_update_api_view(self):
        """
        Проверка обновления данных питомца через api-pet
        """
        weight = 25.0
        # для того, что бы Python передал данные не как словарь, а как json
        post_data_json = json.dumps({'name': self.pet.name, 'sex': self.pet.sex, 'weight': weight})
        response = self.client.put(reverse('profileapp:pet-detail', kwargs={'pk': self.pet.pk}), post_data_json,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()
        pet = Pet.objects.get(name=PetProfileTestCase.create_data['name'], owner=self.user)
        self.assertEqual(pet.weight, weight)

    def test_pet_detail_api_view(self):
        """
        Проверка отображения детальной информации о питомце с помощью api-pet
        """
        response = self.client.get(reverse('profileapp:pet-detail', kwargs={'pk': self.pet.pk}))
        self.assertEqual(response.status_code, 200)

        expected_data = APIPetTestCase.create_data
        expected_data['id'] = self.pet.pk
        expected_data['birth'] = None
        expected_data['chip'] = None
        expected_data['tatoo'] = ""
        expected_data['date_tatoo'] = None
        expected_data['passport'] = None
        expected_data['avatar'] = None
        expected_data['weight'] = None

        # Преобразуем контент ответа в словарь
        response_data = json.loads(response.content)

        self.assertEqual(response_data, expected_data)

    def test_pet_delete_api_view(self):
        """
        Проверка удаления пользователя с помощью api-pet
        """
        response = self.client.delete(reverse('profileapp:pet-detail', kwargs={'pk': self.pet.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Pet.objects.filter(name=self.pet.name, owner=self.user).exists())
