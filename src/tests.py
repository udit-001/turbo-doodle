import unittest
from copy import deepcopy

from flask_testing import TestCase

from app import app
from init_tree import create_tree


class BaseTestCase(TestCase):
    INSERT_URL = "/v1/insert"
    SEARCH_URL = "/v1/query"

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        global tree
        tree = create_tree()

    def tearDown(self):
        del globals()['tree']


class SearchQueryTest(BaseTestCase):
    def test_search(self):
        data = {
            "dim": [
                {
                    "key": "country",
                    "val": "IN"
                }
            ]
        }
        response = self.client.get(
            self.SEARCH_URL, json=data, content_type='application/json')
        if response.status_code == 200:
            self.assert200(response)
            self.assertListEqual(data["dim"], response.json["dim"])
        else:
            self.assert404(response)
            self.assertEqual(response.json, {"detail": "Not Found"})

    def test_search_no_result(self):
        data = {
            "dim": [
                {
                    "key": "country",
                    "val": "KR"
                }
            ]
        }
        response = self.client.get(
            self.SEARCH_URL, json=data, content_type='application/json')
        self.assert404(response)

class InsertNodeTests(BaseTestCase):
    def test_add_new_country(self):
        data = {
            "dim": [
                {"key": "country", "val": "UK"}
            ],
            "metrics": [
                {
                    "key": "webreq",
                    "val": 20
                },
                {
                    "key": "timespent",
                    "val": 30
                }
            ]
        }
        response = self.client.post(self.INSERT_URL,
                                    json=data, content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json, data)

    def test_add_new_country_device(self):
        data = {
            "dim": [
                {
                    "key": "country",
                    "val": "TR"
                },
                {
                    "key": "device",
                    "val": "mobile"
                }
            ],
            "metrics": [
                {
                    "key": "webreq",
                    "val": 70
                },
                {
                    "key": "timespent",
                    "val": 30
                }
            ]
        }
        response = self.client.post(self.INSERT_URL,
                                    json=data, content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json, data)

        # Parent Search Data
        parent_data = deepcopy(data)
        parent_data.pop('metrics')
        parent_data['dim'].pop()
        search_response = self.client.get(
            self.SEARCH_URL, json=parent_data, content_type='application/json')
        self.assert200(search_response)
        self.assertEqual(search_response.json['dim'], parent_data['dim'])

    def test_update_old_metrics(self):
        data = {
            "dim": [
                {
                    "key": "country",
                    "val": "IN"
                },
                {
                    "key": "device",
                    "val": "mobile"
                }
            ],
            "metrics": [
                {
                    "key": "webreq",
                    "val": 70
                },
                {
                    "key": "timespent",
                    "val": 30
                }
            ]
        }
        response = self.client.post(self.INSERT_URL,
                                    json=data, content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json['dim'], data['dim'])
        self.assertGreaterEqual(
            response.json['metrics'][0]['val'], data['metrics'][0]['val'])
        self.assertGreaterEqual(
            response.json['metrics'][1]['val'], data['metrics'][1]['val'])

    def test_partial_update_old_metrics(self):
        data = {
            "dim": [
                {
                    "key": "country",
                    "val": "IN"
                },
                {
                    "key": "device",
                    "val": "mobile"
                }
            ],
            "metrics": [
                {
                    "key": "webreq",
                    "val": 70
                }
            ]
        }
        response = self.client.post(self.INSERT_URL,
                                    json=data, content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json['dim'], data['dim'])
        self.assertGreaterEqual(
            response.json['metrics'][0]['val'], data['metrics'][0]['val'])

    def test_check_parent_metric_update(self):
        data = {
            "dim": [
                {"key": "country", "val": "IN"}
            ]
        }
        parent_query = self.client.get(self.SEARCH_URL,
                                       json=data, content_type='application/json')
        self.assert200(parent_query)
        new_node_data = {
            "dim": [
                {
                    "key": "country",
                    "val": "IN"
                },
                {
                    "key": "device",
                    "val": "tablet"
                }
            ],
            "metrics": [
                {
                    "key": "webreq",
                    "val": 200
                },
                {
                    "key": "timespent",
                    "val": 100
                }
            ]
        }
        response = self.client.post(
            self.INSERT_URL, json=new_node_data, content_type="application/json")
        self.assert200(response)

        parent_update = self.client.get(
            self.SEARCH_URL, json=data, content_type="application/json")
        self.assert200(parent_update)

        old_data = parent_query.json
        updated_data = parent_update.json
        self.assertEqual(updated_data['metrics'][0]['val'], old_data['metrics']
                         [0]['val'] + new_node_data['metrics'][0]['val'])
        self.assertEqual(updated_data['metrics'][1]['val'], old_data['metrics']
                         [1]['val'] + new_node_data['metrics'][1]['val'])



class APIValidationTests(BaseTestCase):
    def test_search_malformed_json(self):
        data = '{"dim": [}'
        response = self.client.get(
            self.SEARCH_URL, data=data, content_type="application/json")
        self.assert400(response)

    def test_insert_malformed_json(self):
        data = '{"metrics": [}'
        response = self.client.post(
            self.INSERT_URL, data=data, content_type="application/json")
        self.assert400(response)

    def test_search_api_empty_dims(self):
        data = {
            "dims": []
        }
        response = self.client.get(
            self.SEARCH_URL, json=data, content_type="application/json")
        self.assert400(response)

    def test_search_api_invalid_type(self):
        data = {
            "dims": [
                {
                    "key": 23,
                    "val": 34
                }
            ]
        }
        response = self.client.get(
            self.SEARCH_URL, json=data, content_type="application/json")
        self.assert400(response)

    def test_insert_api_missing_metrics(self):
        data = {
            "dim": [
                {
                    "key": "country",
                    "val": "IN"
                },
                {
                    "key": "device",
                    "val": "mobile"
                }
            ],
        }
        response = self.client.post(
            self.INSERT_URL, json=data, content_type="application/json")
        self.assert400(response)
        self.assertEqual("metrics" in response.json, True)

    def test_insert_api_missing_dim(self):
        data = {
            "metrics": [
                {
                    "key": "webreq",
                    "val": 70
                },
                {
                    "key": "timespent",
                    "val": 30
                }
            ]
        }
        response = self.client.post(
            self.INSERT_URL, json=data, content_type="application/json")
        self.assert400(response)
        self.assertEqual("dim" in response.json, True)


if __name__ == '__main__':
    unittest.main()
