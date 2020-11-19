# graphql_test_repo
Retrieve top repo stats using API calls with Graphql to Github using

Overview:

This was a fun project. 

I originally wanted to try the classic API call mechanism to Github but found it retrieved too much data with each query. Also I would have to use different API endpoints to get stargazers and forks counts vs PR counts.

For example to use this query: curl https://api.github.com/search/repositories?q=org:twitter, would retrieve so much extraneous than I needed.

I did some more searching and found that the next generation API calling framework was GraphQL.

This worked out a lot better and queries could be accomplished against one endpoint.


Requirements:

This was developed on Python 3. I used Python 3.7 and used some common modules for developing this command line application.

There is a requirements.txt file in the root folder listing some of the required modules.



How to run on the command line:

NOTE: You will need to run this with your own Github access token

./github_query_driver.py organization twitter N 5 token [your token here]

required parameters:

1. organization. Plug your organization name after this parameter
2. N the number of top results to return. Must be an integer
3. Your personal access token to use this tool which will be passed to the GraphQL API endpoint

TODOS:

There are plenty of TODOS here but further refactoring and cleanup would be advantageous.

I had to timebox this effort since I have other obligations in my workweek.