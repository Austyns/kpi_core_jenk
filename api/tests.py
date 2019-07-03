from django.test import TestCase
<<<<<<< HEAD
from rest_framework.test import APIRequestFactory, RequestsClient, APITestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
# from models import System_users
# from api import views
from requests.auth import HTTPBasicAuth

=======
>>>>>>> 877893f7a98f908270bb5adb4f51ca251064d96c
from api.models import Department


class DepartmentTest(TestCase):
    """ Test module for Department model """
<<<<<<< HEAD
=======

>>>>>>> 877893f7a98f908270bb5adb4f51ca251064d96c
    def setUp(self):
        Department.objects.create(
            name='Casper', description='Casper Department')
        Department.objects.create(
            name='Muffin', description='Muffin Department')

    def test_Department_description(self):
        Department_casper = Department.objects.get(name='Casper')
        Department_muffin = Department.objects.get(name='Muffin')
        self.assertEqual(
            Department_casper.description, "Casper Department")
        self.assertEqual(
            Department_muffin.description, "Muffin Department")


<<<<<<< HEAD
    def test_authentication_of_requests(self):
        client = RequestsClient()
        """
        Test that requests are authenticated.
        """
        data = {'name': 'testName', 'description' : 'test-description' }
        response = client.post('http://localhost:8000/api/departments/', data)
        print("Authorization verifying ", response )
        # status code shold be 401 Unauthorized since not autorized        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Authorization verified",response)



    def test_create_department(self):
        client = RequestsClient()
        client.auth = HTTPBasicAuth('admins', 'pass1234')
        """
        Test that a System_user Account can be created.
        """
        # url = reverse('api:systemAdmins')
        data = {'name': 'testName', 'description' : 'test-description' }
        response = client.post('http://localhost:8000/api/departments/', data)
        # print response;
        
        self.assertEqual(Department.objects.all.count(), 1)

=======
>>>>>>> 877893f7a98f908270bb5adb4f51ca251064d96c
