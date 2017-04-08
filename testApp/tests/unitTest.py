from django.test import TestCase, Client
from ..models import TestModel
from ..forms import TestModelForm
from django.core.urlresolvers import reverse
from ..fetch_data import fetch_data
from rest_framework.test import APITestCase
from rest_framework import status

# Set of generic tests, be aware that the self.client of the api test is a member of ApiTestCase.


class ModelTest(TestCase):
    """TestModel test"""
    def test_test_model(self):
        test_model = TestModel.objects.create(text='Hello there', title='Hello World')
        self.assertEqual(test_model.title, 'Hello World')
        self.assertTrue(isinstance(test_model, TestModel))
        self.assertEqual(str(test_model), 'Hello World')


class ViewsTest(TestCase):
    """Test show_page GET/POST request"""
    # Client is a django test class that mimics a client to allow the making of requests
    # Reverse is a utility that allows us to refer to a url by its name (see url.py for names)
    def setUp(self):
        self.client = Client()

    def test_get_page(self):
        response = self.client.get(reverse('home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['name'], 'jack')

    def test_post_page(self):
        response = self.client.post(reverse('home_page'), data={'text': 'Hello there',
                                                                'title': 'Hello World'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['success'], True)

    def test_post_page_invalid_data(self):
        response = self.client.post(reverse('home_page'), data={'text': '',
                                                                'title': ''})
        self.assertEqual(response.context['success'], False)


class FormTest(TestCase):
    """Test TestModelForm validation"""
    def test_test_model_form_valid(self):
        form = TestModelForm(data={'text': 'Hello there',
                                   'title': 'Hello world'})
        self.assertTrue(form.is_valid())

    def test_test_model_form_invalid(self):
        form = TestModelForm(data={'text': '',
                                   'title': ''})
        self.assertFalse(form.is_valid())


class FetchDataTest(TestCase):
    """Test fetching of api data"""
    def test_get_data(self):
        response = fetch_data('http://echo.jsontest.com/key/value')
        self.assertEqual(response.data['key'], 'value')
        self.assertTrue(response.status)

    def test_get_dat_fails_gracefully(self):
        response = fetch_data('this_is-a_malformed_URL')
        self.assertFalse(response.status)


class ApiTest(APITestCase):
    """Test the api endpoint"""
    def setUp(self):
        self.test_model1 = TestModel.objects.create(title='Hi there', text='how\'s it going')
        self.test_model2 = TestModel.objects.create(title='Bye Bye', text='later\'s')

    def test_test_model_get_all_filtered_by_titles(self):
        response = self.client.get(reverse('test_models-list') + '?titles[]={}'.format(self.test_model1.title))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Hi there')

    def test_test_model_get_all(self):
        response = self.client.get(reverse('test_models-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, 'Bye Bye')
        self.assertContains(response, 'Hi there')

    def test_test_model_get_by_pk(self):
        # django-rest-api routers create several url patterns, reverse them by appending either -list or -detail
        # kwargs allows us to insert params into the url
        response = self.client.get(reverse('test_models-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Hi there')






