#!/usr/bin/env python3

import constants
import query_class

from docopt import docopt
args = docopt(constants.usage)
print(args)
print(args['<name>'])

this_query = query_class.QueryClass(args['<hash>'], passed_count=args['<count>'])
this_query.make_query()
json_data = this_query.return_json_data()

this_query.gather_repo_stat_counts()
this_query.list_results()

print("*** start ***")

page_info = this_query.get_page_info(json_data)
print(page_info)
this_query.query_pagination(page_info)

this_query.set_query()
this_query.make_query()
json_data2 = this_query.return_json_data()

this_query.gather_repo_stat_counts()
this_query.list_results()

this_query.print_repo_counts()

this_query.calculate_top_counts()
this_query.print_top_counts()

this_query.calculate_top_contribution_repos()
this_query.print_top_repo_contributors()

print("*** end ***")

