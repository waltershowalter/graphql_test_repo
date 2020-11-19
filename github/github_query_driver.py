#!/usr/bin/env python3

"""
Driver class for getting top repos from
"""
__author__='Andrew.Fernandez'

import constants
import query_class
import logging
import logging.config
import test_logging_mixin
from docopt import docopt


class GitHubQueryDriver(test_logging_mixin.TestLoggingMixin):

    def __init__(self):
        """Initialize the class

        """
        super().__init__()
        self.args = docopt(constants.USAGE)

    def run_query(self) -> None:
        """Runs the query and gets the stats requested from the exercise

        :return: None
        """

        print("*** TOP RESULTS ***")

        assert len(self.args['<hash>'] ) == 40
        assert str(self.args['<count>']).isdigit()

        this_query = query_class.QueryClass(self.args['<hash>'], passed_count=self.args['<count>'])
        this_query.make_query()
        json_data = this_query.json_data

        this_query.gather_repo_stat_counts()

        page_info = this_query.get_page_info(json_data)
        this_query.query_pagination(page_info)

        this_query.set_query()
        this_query.make_query()

        this_query.gather_repo_stat_counts()

        this_query.calculate_top_counts()
        this_query.output_top_counts()

        this_query.calculate_top_contribution_repos()
        this_query.output_top_repo_contributors()


gqd = GitHubQueryDriver()
gqd.run_query()