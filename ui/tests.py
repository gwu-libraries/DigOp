from django.test import TestCase
from ui.models import Project

class ProjectViewsTestCase(TestCase):
    fixtures = ['project_view_testdata.json']

    def test_index(self):
        resp = self.client.get('/show_projects/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('rows' in resp.context)
        self.assertEqual([project.pk for project in resp.context['rows']], [1])

        # Ensure that non-existent projects throw a 404.
        resp = self.client.get('/project_data/4/')
        self.assertEqual(resp.status_code, 404)
