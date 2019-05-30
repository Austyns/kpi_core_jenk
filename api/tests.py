from django.test import TestCase
from api.models import Department


class DepartmentTest(TestCase):
    """ Test module for Department model """

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


