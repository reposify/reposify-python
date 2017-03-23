import reposify
import os
import unittest
import requests
from urllib.parse import urlparse
from mock import patch


class ReposifyUnitTest(unittest.TestCase):
    @staticmethod
    def _mock_request(url):
        path = urlparse(url).path
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

    def setUp(self):
        def mock_get(url, params):
            return self._mock_request(url)

        def mock_post(url, params, data):
            return self._mock_request(url)

        self.get_patch = patch('reposify.requests.get', mock_get)
        self.post_patch = patch('reposify.requests.post', mock_post)
        self.get_patch.start()
        self.post_patch.start()

    def tearDown(self):
        self.get_patch.stop()
        self.post_patch.stop()

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
        results = insights.count(banner="test", filters="country_name:Sudan")

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

    def test_discovery_internet(self):
        discovery = reposify.Discovery(token='mock_token')
        response = discovery.internet(port=25, protocol='smtp')

        self.assertIn('job_id', response)
        self.assertIn('ips', response)
        self.assertIn('status', response)

        self.assertEqual(response['job_id'], 'dc233e85-91ce-4f0c-a438-98fc4228731b')
        self.assertEqual(response['ips'], '*')
        self.assertEqual(response['status'], 'pending')

    def test_discovery_host(self):
        discovery = reposify.Discovery(token='mock_token')
        response = discovery.host(port=25, protocol='smtp', ip_addresses='208.130.29.0/24')

        self.assertIn('job_id', response)
        self.assertIn('ips', response)
        self.assertIn('status', response)

        self.assertEqual(response['job_id'], '7448dc4d-5313-400f-bc02-17f40ebf2f84')
        self.assertEqual(response['ips'], '208.130.29.0/24')
        self.assertEqual(response['status'], 'pending')

    def test_discovery_status(self):
        discovery = reposify.Discovery(token='mock_token')
        scan_status = discovery.status(job_id='6c506856-2d74-4329-b9bc-95257afb2264')

        self.assertIn('status', scan_status)
        self.assertIn('job_id', scan_status)
        self.assertIn('last_ip_scanned', scan_status)
        self.assertIn('created_date', scan_status)
        self.assertIn('ips_left_to_be_scanned', scan_status)

        self.assertEqual(scan_status['status'], "processing")
        self.assertEqual(scan_status['job_id'], '6c506856-2d74-4329-b9bc-95257afb2264')
        self.assertEqual(scan_status['last_ip_scanned'], '208.130.29.0')
        self.assertEqual(scan_status['created_date'], '2017-03-01T16:50:08.906Z')
        self.assertEqual(scan_status['ips_left_to_be_scanned'], 256)

if __name__ == '__main__':
    unittest.main()
