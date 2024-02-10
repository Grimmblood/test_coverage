from unittest import TestCase

import src.counter
from src.counter import app
from src import status
"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""


class CounterTest(TestCase):
    """ Counter Tests """

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """ Should create a counter """
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_counter(self):
        """ It should return an error for duplicates """
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_counter(self):
        result = self.client.put('/counters/testCounter')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

        # Create a counter
        result = self.client.post('/counters/testCounter')

        # Ensure that it returned a successful return code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # check the counter value as a baseline
        result_base = result.get_data(True)
        # call to update the counter I just created
        result = self.client.put('/counters/testCounter')

        # ensure that it returned a successful return code
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        # check that the counter value is one more than the baseline measured earlier
        # self.assertEqual(result_base, result.get_data(True))

    def test_read_counter(self):
        result = self.client.get('/counters/testReadCounter')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

        # create a counter
        result = self.client.post('/counters/testReadCounter')

        # ensure successful error code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # update the counter
        result = self.client.put('/counters/testReadCounter')

        # check the counter value
        result = self.client.get('/counters/testReadCounter')

        # ensure a successful error code
        self.assertEqual(result.status_code, status.HTTP_200_OK)