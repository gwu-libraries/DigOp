from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse

from ui.models import Project
from ui.models import Item
from ui.models import ProcessingSession


class ProjectViewsTestCase(TestCase):
    fixtures = ['all_my_fixtures.json']

    def test_show_projects(self):
        self.client.login(username=settings.TEST_USER,
                          password=settings.TEST_USER_PWD)
        resp = self.client.get('/show_projects/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('rows' in resp.context)

        self.assertIn(1, [item['pk'] for item in resp.context['rows']])

        # Ensure that non-existent projects throw a 404.
        resp = self.client.get('/project_data/4/')
        self.assertEqual(resp.status_code, 404)

    def test_invalid_add_project(self):
        self.client.login(username=settings.TEST_USER,
                          password=settings.TEST_USER_PWD)
        data = {
            'name': 'Test_Project',
            'startDate': '2013-11-13 10:10:23',
            'collection': 'False'
            }
        response = self.client.post(reverse('add_project'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "description",
                             "Enter a value for Project Description")

    def test_valid_add_project(self):
        self.client.login(username=settings.TEST_USER,
                          password=settings.TEST_USER_PWD)
        project_count = Project.objects.count()
        data = {
            'name': 'Test_Project',
            'description': 'Testing add project view',
            'startDate': '2013-11-13 10:10:23.792240',
            'collection': 'False',
            'collections': '38989/c01x7604j831'
            }
        response = self.client.post(reverse('add_project'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), project_count+1)

    def test_add_scan_item(self):
        self.client.login(username=settings.TEST_USER,
                          password=settings.TEST_USER_PWD)
        item_count = Item.objects.count()
        data = {
            'project': '1',
            'barcode': '32882017694412',
            'itemType': 'Book'
            }
        response = self.client.post(reverse('process_book_form'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.count(), item_count+1)
        session_count = ProcessingSession.objects.count()
        data = {
            'itemType': 'Book',
            'item': '32882017694412',
            'task': 'Scan',
            'operationComplete': '2',
            'startTime': '2013-11-13 11:34:47.618946',
            'endTime': '2013-11-13 12:34:47.618946',
            'pagesDone': '250',
            'comments': 'Done'
            }
        response = self.client.post(reverse('process_processing_form'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProcessingSession.objects.count(), session_count+1)
