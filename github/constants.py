"""Github test project constants"""

USAGE = """
Github API tester.

Usage:
  github_query_driver.py organization <name> N <count> token <hash>

Options:
  -h --help     Show this screen.
"""

GRAPHQL_URL = 'https://api.github.com/graphql'

MOCK_JSON_DATA = """
{
  "data": {
    "organization": {
      "repositories": {
        "pageInfo": {
          "hasNextPage": true,
          "startCursor": "Y3Vyc29yOnYyOpHOAATGJQ==",
          "endCursor": "Y3Vyc29yOnYyOpHOAAjTgw=="
        },
        "nodes": [
          {
            "name": "hadoop-lzo",
            "pullRequests": {
              "totalCount": 78
            },
            "forks": {
              "totalCount": 187
            },
            "stargazers": {
              "totalCount": 515
            }
          },
          {
            "name": "thrift_client",
            "pullRequests": {
              "totalCount": 45
            },
            "forks": {
              "totalCount": 72
            },
            "stargazers": {
              "totalCount": 194
            }
          },
          {
            "name": "twurl",
            "pullRequests": {
              "totalCount": 61
            },
            "forks": {
              "totalCount": 247
            },
            "stargazers": {
              "totalCount": 1477
            }
          },
          {
            "name": "elephant-bird",
            "pullRequests": {
              "totalCount": 360
            },
            "forks": {
              "totalCount": 341
            },
            "stargazers": {
              "totalCount": 1099
            }
          }
        ]
      }
    }
  }
}
"""