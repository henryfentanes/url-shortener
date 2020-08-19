from django.test import TestCase
from core.models import ShortenedURL


class TestShortenedURLModel(TestCase):

    def test_shortened_url_is_generated_automatically(self):
        obj = ShortenedURL.objects.create(expanded_url='https://google.com')
        self.assertTrue(obj.shortened_url)

    def test_shortened_url_auto_generates_unique_codes(self):
        obj = ShortenedURL.objects.create(expanded_url='https://google.com')
        # Try and force a second ShortnedURL with a repeated code
        obj_2 = ShortenedURL.objects.create(
            expanded_url='https://google.com',
            shortened_url=obj.shortened_url)
        # Assert the code got automatically adjusted to a unique one
        self.assertNotEqual(obj.shortened_url, obj_2.shortened_url)


class TestShortenURLForm(TestCase):

    def test_shortened_url_returns_in_response_content(self):
        resp = self.client.post('/', {'expanded_url': 'https://google.com'})
        result = resp.context_data.get('result')
        self.assertIn(result, str(resp.content))

    def test_user_can_shorten_their_full_url(self):
        resp = self.client.post('/', {'expanded_url': 'https://google.com'})
        result = resp.context_data.get('result')
        self.assertTrue(
            ShortenedURL.objects.get(shortened_url=result.split('/')[-1]))

    def test_error_returns_in_result_response_content(self):
        resp = self.client.post('/', {'expanded_url': ''})
        self.assertIn("Fill one of the input fields above.", str(resp.content))


class TestRedirectShortenedURLToFullURL(TestCase):

    def test_client_gets_redirected_to_full_url_based_on_shortened_one(self):
        obj = ShortenedURL.objects.create(expanded_url='https://google.com')
        resp = self.client.get(f'/{obj.shortened_url}')
        # Assert client gets permanent redirect
        self.assertEqual(301, resp.status_code)
        self.assertEqual(obj.expanded_url, resp.url)

