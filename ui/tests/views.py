from django.test import TestCase
from django.conf import settings

from ui.models import Project

class ProjectViewsTestCase(TestCase):
    fixtures = ['all_my_fixtures.json']

    def test_index(self):
        self.client.login(username=settings.TEST_USER, password= settings.TEST_USER_PWD)
        resp = self.client.get('/show_projects/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('rows' in resp.context)

        self.assertIn(1, [item['pk'] for item in resp.context['rows']])

        # Ensure that non-existent projects throw a 404.
        resp = self.client.get('/project_data/4/')
        self.assertEqual(resp.status_code, 404)
