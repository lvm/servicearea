import re
import json
import random
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from faker import Faker
from pathlib import Path

from world_class import Languages
from world_class import Currencies


def load_test_data():
    data_file = Path(__file__).parent / "test_data/countries_sample.geojson"
    data = json.load(open(data_file, "r"))
    countries = {}
    return [
        {"name": d.get("properties").get("ADMIN"), "area": d.get("geometry")}
        for d in data
    ]


class ProviderTestCase(APITestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self._username = "admin"
        self._password = "admin"
        self._email = "admin@admin.admin"
        self.user = self.UserModel.objects.create_superuser(
            *[getattr(self, f"_{attr}") for attr in ["username", "email", "password"]]
        )
        self.token = Token.objects.create(user=self.user)
        self.client.force_login(user=self.user)

        self.faker = Faker()
        self.area_data = load_test_data()
        self.provider_data = [self._gen_provider() for x in range(10)]

    def _gen_provider(self):
        return dict(
            name=f"{self.faker.company()} {self.faker.company_suffix()}",
            email=self.faker.email(),
            phone_number="+12125552368",
            language=self._choose_language(),
            currency=self._choose_currency(),
        )

    def _choose_thing(self, thing):
        thing_list = list(thing)
        index = random.randint(0, len(thing_list) - 1)
        return thing_list[index]

    def _choose_language(self):
        return self._choose_thing(Languages()).code

    def _choose_currency(self):
        return self._choose_thing(Currencies()).code

    def _choose_price(self):
        return round(random.uniform(100,10000), 4)

    def _choose_provider(self):
        return self._choose_thing(self.provider_data)

    def _choose_area(self):
        return self._choose_thing(self.area_data)
    def _create_provider(self):
        data = self._choose_provider()
        return self.client.post(reverse("provider-list"), data=data)

    def _create_servicearea(self):
        response = self._create_provider()
        provider_pk = response.json().get("id")

        data = self._choose_area()
        data.update({"price": self._choose_price(), "provider": provider_pk})
        return self.client.post(reverse("servicearea-list"), data=data)

    def test_create_provider(self):
        response = self._create_provider()
        self.assertEqual(response.status_code, 201)

    def test_get_provider(self):
        response = self._create_provider()
        pk = response.json().get("id")

        response = self.client.get(reverse("provider-detail", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 200)

    def test_update_provider(self):
        response = self._create_provider()
        pk = response.json().get("id")

        data = {"name": f"{self.faker.company()} {self.faker.company_suffix()}"}
        response = self.client.patch(
            reverse("provider-detail", kwargs={"pk": pk}), data=data
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_provider(self):
        response = self._create_provider()
        pk = response.json().get("id")

        response = self.client.delete(reverse("provider-detail", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 204)

    def test_create_servicearea(self):
        response = self._create_servicearea()
        self.assertEqual(response.status_code, 201)

    def test_get_servicearea(self):
        response = self._create_servicearea()
        pk = response.json().get("id")

        response = self.client.get(reverse("servicearea-detail", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 200)

    def test_update_servicearea(self):
        response = self._create_servicearea()
        pk = response.json().get("id")

        data = self._choose_area()
        response = self.client.patch(
            reverse("servicearea-detail", kwargs={"pk": pk}), data=data
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_servicearea(self):
        response = self._create_servicearea()
        pk = response.json().get("id")

        response = self.client.delete(reverse("servicearea-detail", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 204)
