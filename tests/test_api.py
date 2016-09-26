import reposify
import os
import unittest
import requests

try:
    import urlparse
except ImportError:
    from urllib.parse import urlparse

from mock import patch


class ReposifyUnitTest(unittest.TestCase):
    def setUp(self):
        def mock_get(url, params):
            path = urlparse.urlparse(url).path
            path_tuple = os.path.split(path)
            endpoint = path_tuple[0].replace('/v1/', '').split('/')
            endpoint = '_'.join(endpoint)

            if len(path_tuple) > 1:
                endpoint += '_' + path_tuple[1]

            mock_response_file = os.path.normpath('tests/mock_get_responses/%s.json' % endpoint)
            with open(mock_response_file, mode='rb') as response_file:
                as_json = response_file.read()

            response = requests.Response()
            response._content = as_json
            response.status_code = 200

            return response

        self.get_patch = patch('reposify.requests.get', mock_get)
        self.get_patch.start()

    def tearDown(self):
        self.get_patch.stop()

    def test_insights_search(self):
        insights = reposify.Insights(token='mock_token')
        results = insights.search(banner="test", filters="port:80")

        self.assertIn('entities', results)
        self.assertEqual(results['entities'], [])

        self.assertIn('pagination', results)
        self.assertIn('has_more', results['pagination'])
        self.assertIn('page', results['pagination'])
        self.assertIn('page_count', results['pagination'])
        self.assertIn('total_pages', results['pagination'])
        self.assertIn('urls', results['pagination'])

        self.assertEqual(results['pagination']['has_more'], False)
        self.assertEqual(results['pagination']['page'], 1)
        self.assertEqual(results['pagination']['page_count'], 0)
        self.assertEqual(results['pagination']['total_pages'], 0)
        self.assertEqual(results['pagination']['urls'], {'next': None, 'prev': None})

        self.assertIn('total_count', results)
        self.assertEqual(results['total_count'], 0)

    def test_insights_count(self):
        insights = reposify.Insights(token='mock_token')
        results = insights.count(banner="test", filters="country:us")

        self.assertIn('total_count', results)
        self.assertEqual(results['total_count'], 10000)

    def test_account_status(self):
        account = reposify.Account(token='mock_token')
        account_status = account.status()

        self.assertIn('plan', account_status)
        self.assertIn('insights_credits', account_status)
        self.assertIn('scan_credits', account_status)

        self.assertEqual(account_status['plan'], "Free")
        self.assertEqual(account_status['insights_credits'], 4000)
        self.assertEqual(account_status['scan_credits'], 2000)

if __name__ == '__main__':
    unittest.main()
