#!/usr/bin/env python3
""" Parameterize and patch as decorators """
import unittest
from typing import List, Dict
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock, MagicMock
from requests import HTTPError
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ TestGithubOrgClient class """
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org: str,
                 response: Dict, mock_get_json: MagicMock) -> None:
        """ Test org """
        mock_get_json.return_value = MagicMock(return_value=response)
        client = GithubOrgClient(org)
        self.assertEqual(client.org(), response)
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org))

    def test_public_repos_url(self) -> None:
        """ Test public repos URL """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "://https://api.github.com/users/google/repos"}
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url,
                             "https://api.github.com/orgs/google/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """ Test public repos URL """
        test_payload = {
            "repos_url": "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-22T20:05:46Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "pushed_at": "2019-09-23T11:53:57Z",
                    "homepage": "",
                    "has_issues": True,
                    "has_projects": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 7776515,
                    "name": "cpp-netlib",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": True,
                    "url": "https://api.github.com/repos/google/cpp-netlib",
                    "created_at": "2013-01-29T19:15:47Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "pushed_at": "2019-09-23T11:53:57Z",
                    "homepage": "",
                    "has_issues": False,
                    "has_projects": True,
                    "forks": 59,
                    "default_branch": "master",
                }
            ]
        }
        mock_get_json.return_value = test_payload['repos']
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload['repos_url']
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), test_payload['repos'])
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "bsl-1.0"}}, "bsl-1.0", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        " Test has license"
        client = GithubOrgClient("google")
        client_has_license = client.has_license(repo, key)
        self.assertEqual(client_has_license, expected)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos',
                      'apache2_repos'),
                     TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ TestIntegrationGithubOrgClient class """
    @classmethod
    def setUpClass(cls) -> None:
        """ Set up class """
        conf = {"return_value.json.side_effect": [
            cls.org_payload, cls.repos_payload,
            cls.org_payload, cls.repos_payload
        ]}
        cls.get_patcher = patch('requests.get', **conf)
        cls.mock = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """ Tear down class """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """ Test public repos """
        client = GithubOrgClient("google")
        self.assertEqual(client.org(), self.org_payload)
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """ Test public repos with license """
        client = GithubOrgClient("google")
        self.assertEqual(client.org(), self.org_payload)
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
        self.mock.assert_called()
