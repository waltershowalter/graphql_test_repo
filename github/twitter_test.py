#!/usr/bin/env python3

import requests
import json

usage="""
Github API tester.

Usage:
  twitter_test.py org_name <id> count <count>
  
Options:
  -h --help     Show this screen.
"""
from docopt import docopt
args = docopt(usage)
print(args)
print(args['<id>'])

query = (
  f"{{"
  f"search(query: \"org:{args['<id>']} stars:>=0 sort:stars\", type: REPOSITORY, first: {args['<count>']}) {{"
  f"  repositoryCount"
  f"  edges {{"
  f"    node {{"
  f"      ... on Repository {{"
  f"        name"
  f"        descriptionHTML"
  f"        stargazers {{"
  f"          totalCount"
  f"        }}"
  f"        forks {{"
  f"          totalCount"
  f"        }}"
  f"        pullRequests {{"
  f"          totalCount"
  f"        }}"
  f"        updatedAt"
  f"      }}"
  f"    }}"
  f"  }}"
  f"}}"
  f"}}"
)

url = 'https://api.github.com/graphql'
headers = {'Authorization': 'Bearer your_passed_in_string_here'}
response = requests.post(url, headers=headers, json={'query': query})
print(response.status_code)
print(response.text)
json_data = json.loads(response.text)
print(json_data['data']['search']['edges'])

repo_stars = {node['node']['name']: node['node']['stargazers']['totalCount'] for node in json_data['data']['search']['edges']}

for key, value in repo_stars.items():
    print("Repo: {}, stars {}".format(key, value))

# for current_node in json_data['data']['search']['edges']:
#    print("Stargazers count: {}".format(current_node['node']['stargazers']['totalCount']))

