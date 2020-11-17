#!/usr/bin/env python3

import requests
import json

usage="""
Github API tester.

Usage:
  twitter_pr_test.py organization <name> N <count>
  
Options:
  -h --help     Show this screen.
"""
from docopt import docopt
args = docopt(usage)
print(args)
print(args['<name>'])

query = (
  f"{{"
  f"organization(login: \"{args['<name>']}\") {{"
  f"  repositories(first:100) {{"
  f"    pageInfo {{"
  f"      hasNextPage"
  f"      startCursor"
  f"      endCursor"
  f"  	}}"
  f"    nodes {{"
  f"      name"
  f"      pullRequests {{"
  f"        totalCount"
  f"      }}"
  f"      forks {{"
  f"        totalCount"
  f"      }}"
  f"      stargazers {{"
  f"        totalCount"
  f"      }}"  
  f"    }}"
  f"    }}"
  f"  }}"
  f"}}"
  )

url = 'https://api.github.com/graphql'
headers = {'Authorization': 'Bearer 10def6642b0df216b2bff51829c341013948a206'}


response = requests.post(url, headers=headers, json={'query': query})
print(response.status_code)
print(response.text)
json_data = json.loads(response.text)

repo_stars = {node['name']: node['stargazers']['totalCount'] for node in json_data['data']['organization']['repositories']['nodes']}
repo_forks = {node['name']: node['forks']['totalCount'] for node in json_data['data']['organization']['repositories']['nodes']}
repo_prs = {node['name']: node['pullRequests']['totalCount'] for node in json_data['data']['organization']['repositories']['nodes']}

for key, value in repo_stars.items():
    print("Repo: {}, stars {}".format(key, value))


print("********")
pageInfo = json_data['data']['organization']['repositories']['pageInfo']
print(pageInfo)

after_string = ""

if pageInfo['hasNextPage']:
    cursor_hash = pageInfo['endCursor']
    print("What is the cursor hash: {}".format(cursor_hash))
    after_string = ", after:\"{}\"".format(cursor_hash)

query2 = (
  f"{{"
  f"organization(login: \"twitter\") {{"
  f"  repositories(first:100{after_string} ) {{"
  f"    pageInfo {{"
  f"      hasNextPage"
  f"      startCursor"
  f"      endCursor"
  f"  	}}"
  f"    nodes {{"
  f"      name"
  f"      pullRequests(states:OPEN) {{"
  f"        totalCount"
  f"      }}"
  f"      forks {{"
  f"        totalCount"
  f"      }}"
  f"      stargazers {{"
  f"        totalCount"
  f"      }}"  
  f"    }}"
  f"    }}"
  f"  }}"
  f"}}"
  )

print(query2)


response2 = requests.post(url, headers=headers, json={'query': query2})
print(response2.status_code)
print(response2.text)

json_data2 = json.loads(response2.text)

repo_stars2 = {node['name']: node['stargazers']['totalCount'] for node in json_data2['data']['organization']['repositories']['nodes']}
repo_forks2 = {node['name']: node['forks']['totalCount'] for node in json_data2['data']['organization']['repositories']['nodes']}
repo_prs2 = {node['name']: node['pullRequests']['totalCount'] for node in json_data2['data']['organization']['repositories']['nodes']}


repo_stars.update(repo_stars2)
repo_forks.update(repo_forks2)
repo_prs.update(repo_prs2)


print("Length of stars: {}".format(len(repo_stars)))
print("Length of forks: {}".format(len(repo_forks)))
print("Length of prs: {}".format(len(repo_prs)))

top_list = sorted(repo_stars.items(), key=lambda x: x[1], reverse=True)[:int(args['<count>'])]
top_list_forks = sorted(repo_forks.items(), key=lambda x: x[1], reverse=True)[:int(args['<count>'])]
top_list_prs = sorted(repo_prs.items(), key=lambda x: x[1], reverse=True)[:int(args['<count>'])]

print(top_list)
print(top_list_forks)
print(top_list_prs)

contribution_dict = {x: round(repo_prs.get(x, 0) / repo_forks.get(x, 0), 2) for x in set(repo_prs).union(repo_forks) if repo_forks.get(x, 0) != 0} 

top_list_contributions = sorted(contribution_dict.items(), key=lambda x: x[1], reverse=True)[:int(args['<count>'])]

print("Length of contribution dictionary: {}".format(len(contribution_dict)))
print(top_list_contributions)

print("*** end ***")

