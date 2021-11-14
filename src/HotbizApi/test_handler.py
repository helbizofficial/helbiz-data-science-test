import boto3
import json
import pytest
from unittest.mock import patch
import unittest
from handler import hotspot, DynamoAccessor

class TestHandler(unittest.TestCase):
    def fake_get_all(self, tableName):
        return [
                {
                    "id": 1,
                },
                {
                    "id": 2
                }
        ]

    @patch.object(DynamoAccessor, 'get_all', fake_get_all)
    def test_handler_returns_ids(self):
        results = hotspot(None, None)
        data = json.loads(results["body"])
        expected_data = [
                {
                    "id": 1
                },
                {
                    "id": 2
                }
        ]

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(data[1]["id"], 2)

    @patch.object(DynamoAccessor, 'get_all', fake_get_all)
    def test_handler_returns_status_code(self):
        results = hotspot(None, None)

        self.assertEqual(results["statusCode"], 200)

    @patch.object(DynamoAccessor, 'get_all', fake_get_all)
    def test_handler_returns_headers(self):
        results = hotspot(None, None)

        self.assertEqual(len(results["headers"]), 1)
        self.assertEqual(results["headers"]["Content-Type"], "application/json")
