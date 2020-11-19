"""Query class for graphql"""
__author__='Andrew.Fernandez'

import requests
import json
import constants
import logging
import logging.config
import test_logging_mixin

class QueryClass(test_logging_mixin.TestLoggingMixin):

    def __init__(self, passed_hash, passed_organization="twitter", passed_count=5):
        """Initialize the Query Class

        :param passed_hash:
        :param passed_organization:
        :param passed_count:
        """
        self.url = constants.GRAPHQL_URL
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

    def set_query(self) -> None:
        """Set up of multi-line graphql query

        :return: None
        """
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

    def get_page_info(self, json_data: dict) -> dict:
        """Gets the page-info result node result

        :param json_data:
        :return: None
        """
        page_info = json_data['data']['organization']['repositories']['pageInfo']
        return page_info

    def query_pagination(self, page_info: dict) -> None:
        """Inquries from the response if there's another page

        :param page_info:
        :return: None
        """
        if page_info['hasNextPage']:
            self.has_next_page = True
            cursor_hash = page_info['endCursor']
            # TODO make log statement
            # logging.info("What is the cursor hash: {}".format(cursor_hash))
            self.after_string = ", after:\"{}\"".format(cursor_hash)

    def make_query(self) -> None:
        """Make the query to the graphql API endpoint

        :return: None
        """
        response = requests.post(self.url, headers=self.headers, json={'query': self.github_query})
        self.json_data = json.loads(response.text)

    def create_stargazers_dict(self) -> dict:
        """Retrieve the stargazers count for each repo in the returned org result

        :return: dict
        """
        return {node['name']: node['stargazers']['totalCount'] for node in
                self.json_data['data']['organization']['repositories']['nodes']}

    def create_forks_dict(self) -> dict:
        """Retrieve the forks count for each repo in the returned org result

        :return: dict
        """
        return {node['name']: node['forks']['totalCount'] for node in
                self.json_data['data']['organization']['repositories']['nodes']}

    def create_prs_dict(self) -> dict:
        """Retrieve the stargazers count for each repo in the returned org result

        :return: dict
        """
        return {node['name']: node['pullRequests']['totalCount'] for node in
                self.json_data['data']['organization']['repositories']['nodes']}

    def gather_repo_stat_counts(self) -> None:
        """Create and update the dict counts for the 3 properties for each repo

        :return: None
        """
        if not self.repo_stars and not self.repo_forks and not self.repo_prs:
            self.repo_stars = self.create_stargazers_dict()
            self.repo_forks = self.create_forks_dict()
            self.repo_prs = self.create_prs_dict()
        else:
            self.repo_stars.update(self.create_stargazers_dict())
            self.repo_forks.update(self.create_forks_dict())
            self.repo_prs.update(self.create_prs_dict())

    def output_repo_counts(self) -> None:
        """Output the counts for the stargazers, foks and PRs in each repo

        :return: None
        """
        # logging.info("Length of stars: {}".format(len(self.repo_stars)))
        # logging.info("Length of forks: {}".format(len(self.repo_forks)))
        # logging.info("Length of prs: {}".format(len(self.repo_prs)))
        pass

    def calculate_top_counts(self) -> None:
        """Get the top counts based on the number of top counts to retrive

        :return: None
        """
        self.top_repo_stars = sorted(self.repo_stars.items(), key=lambda x: x[1], reverse=True)[:int(self.count)]
        self.top_repo_forks = sorted(self.repo_forks.items(), key=lambda x: x[1], reverse=True)[:int(self.count)]
        self.top_repo_prs = sorted(self.repo_prs.items(), key=lambda x: x[1], reverse=True)[:int(self.count)]

    def output_top_counts(self) -> None:
        """Output the top counts for each of the fields in each repo

        :return: None
        """
        logging.info("Top repo for stars: {}".format(self.top_repo_stars))
        logging.info("Top repos for forks: {}".format(self.top_repo_forks))
        logging.info("Top repos for PRs: {}".format(self.top_repo_prs))

    def calculate_top_contribution_repos(self) -> None:
        """Calculate the contribution PRs/Forks for the repos

        :return: None
        """
        self.contribution_dict = {x: round(self.repo_prs.get(x, 0) / self.repo_forks.get(x, 0), 2)
                             for x in set(self.repo_prs).union(self.repo_forks) if self.repo_forks.get(x, 0) != 0}
        self.top_repo_contributions = sorted(self.contribution_dict.items(), key=lambda x: x[1],
                                             reverse=True)[:int(self.count)]

    def output_top_repo_contributors(self) -> None:
        """Output the stats for the contribution metric

        :return: None
        """
        # logging.info("Length of contribution dictionary: {}".format(len(self.contribution_dict)))
        logging.info("Top repos for contributions: {}". format(self.top_repo_contributions))

    def list_results(self) -> None:
        """Print the number of stars for the last result query

        :return:
        """
        for key, value in self.repo_stars.items():
            logging.info("Repo: {}, stars {}".format(key, value))

    @property
    def json_data(self) -> dict:
        """Returns the JSON data. Getter

        :return: dict
        """
        return self._json_data

    @json_data.setter
    def json_data(self, value: dict) -> None:
        """Setter for json_data

        :param value: dict
        :return: None
        """
        self._json_data = value

