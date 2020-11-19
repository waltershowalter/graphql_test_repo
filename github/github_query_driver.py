#!/usr/bin/env python3

import constants
import query_class
from docopt import docopt


class GitHubQueryDriver:

    def __init__(self):
        """Initialize the class

        """
        self.args = docopt(constants.USAGE)
        # print(self.args)
        # print(self.args['<name>'])

    def run_query(self) -> None:
        """Runs the query and gets the stats requested from the exercise

        :return: None
        """

        print("*** RESULTS ***")

        assert len(self.args['<hash>'] ) > 35
        assert str(self.args['<count>']).isdigit()

        this_query = query_class.QueryClass(self.args['<hash>'], passed_count=self.args['<count>'])
        this_query.make_query()
        json_data = this_query.json_data

        this_query.gather_repo_stat_counts()
        # this_query.list_results()

        page_info = this_query.get_page_info(json_data)
        this_query.query_pagination(page_info)

        this_query.set_query()
        this_query.make_query()

        this_query.gather_repo_stat_counts()
        # this_query.list_results()

        # this_query.print_repo_counts()

        this_query.calculate_top_counts()
        this_query.print_top_counts()

        this_query.calculate_top_contribution_repos()
        this_query.print_top_repo_contributors()


gqd = GitHubQueryDriver()
gqd.run_query()