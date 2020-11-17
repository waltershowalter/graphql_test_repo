"""Query class for graphql"""

import requests
import json


class QueryClass:

    def __init__(self, passed_hash, passed_organization="twitter", passed_count=5):
        self.url = 'https://api.github.com/graphql'
        self.organization = passed_organization
        self.headers = dict()
        self.headers['Authorization'] = "Bearer " + passed_hash
        self.has_next_page = False
        self.after_string = ""
        self.json_data = ""
        self.github_query = ""
        self.set_query()
        self.repo_stars = None
        self.repo_forks = None
        self.repo_prs = None
        self.contribution_dict = None
        self.count = passed_count
        self.top_repo_stars = None
        self.top_repo_forks = None
        self.top_repo_prs = None
        self.top_repo_contributions = None

    def set_query(self):
        self.github_query = (
            f"{{"
            f"organization(login: \"{self.organization}\") {{"
            f"  repositories(first:100{self.after_string} ) {{"
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

    def get_page_info(self, json_data):
        page_info = json_data['data']['organization']['repositories']['pageInfo']
        return page_info

    def query_pagination(self, page_info):
        if page_info['hasNextPage']:
            self.has_next_page = True
            cursor_hash = page_info['endCursor']
            #TODO make log statement
            # print("What is the cursor hash: {}".format(cursor_hash))
            self.after_string = ", after:\"{}\"".format(cursor_hash)

    def make_query(self):
        response = requests.post(self.url, headers=self.headers, json={'query': self.github_query})
        # print(response.status_code)
        # print(response.text)
        self.json_data = json.loads(response.text)

    def get_stargazers_count(self):
        return {node['name']: node['stargazers']['totalCount'] for node in
                self.json_data['data']['organization']['repositories']['nodes']}

    def get_forks_count(self):
        return {node['name']: node['forks']['totalCount'] for node in
                self.json_data['data']['organization']['repositories']['nodes']}

    def get_prs_count(self):
        return {node['name']: node['pullRequests']['totalCount'] for node in
                self.json_data['data']['organization']['repositories']['nodes']}

    def gather_repo_stat_counts(self):
        if not self.repo_stars and not self.repo_forks and not self.repo_prs:
            self.repo_stars = self.get_stargazers_count()
            self.repo_forks = self.get_forks_count()
            self.repo_prs = self.get_prs_count()
        else:
            self.repo_stars.update(self.get_stargazers_count())
            self.repo_forks.update(self.get_forks_count())
            self.repo_prs.update(self.get_prs_count())

    def print_repo_counts(self):
        print("Length of stars: {}".format(len(self.repo_stars)))
        print("Length of forks: {}".format(len(self.repo_forks)))
        print("Length of prs: {}".format(len(self.repo_prs)))

    def calculate_top_counts(self):
        self.top_repo_stars = sorted(self.repo_stars.items(), key=lambda x: x[1], reverse=True)[:int(self.count)]
        self.top_repo_forks = sorted(self.repo_forks.items(), key=lambda x: x[1], reverse=True)[:int(self.count)]
        self.top_repo_prs = sorted(self.repo_prs.items(), key=lambda x: x[1], reverse=True)[:int(self.count)]

    def print_top_counts(self):
        print("Top stars: {}".format(self.top_repo_stars))
        print("Top forks: {}".format(self.top_repo_forks))
        print("Top PRs: {}".format(self.top_repo_prs))

    def calculate_top_contribution_repos(self):
        self.contribution_dict = {x: round(self.repo_prs.get(x, 0) / self.repo_forks.get(x, 0), 2)
                             for x in set(self.repo_prs).union(self.repo_forks) if self.repo_forks.get(x, 0) != 0}
        self.top_repo_contributions = sorted(self.contribution_dict.items(), key=lambda x: x[1],
                                             reverse=True)[:int(self.count)]

    def print_top_repo_contributors(self):
        # print("Length of contribution dictionary: {}".format(len(self.contribution_dict)))
        print("Top repos for contributions: {}". format(self.top_repo_contributions))

    def list_results(self):
        for key, value in self.repo_stars.items():
            print("Repo: {}, stars {}".format(key, value))

    #TODO make proper property
    def return_json_data(self):
        return self.json_data


