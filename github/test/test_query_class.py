import unittest
import mock
import pytest
import json

from github.query_class import QueryClass
from github.constants import MOCK_JSON_DATA


class TestQueryClass(unittest.TestCase):

    qc = QueryClass("ax05ghx")

    def setup(self):
        self.qc.json_data = None

    def test_create_stargazers_dict(self):
        self.qc.json_data = json.loads(MOCK_JSON_DATA)
        returned_dict = self.qc.create_stargazers_dict()
        assert len(returned_dict) == 4

    def test_create_forks_dict(self):
        self.qc.json_data = json.loads(MOCK_JSON_DATA)
        returned_dict = self.qc.create_forks_dict()
        assert len(returned_dict) == 4

    def test_create_prs_dict(self):
        self.qc.json_data = json.loads(MOCK_JSON_DATA)
        returned_dict = self.qc.create_prs_dict()
        assert len(returned_dict) == 4

