# graphql_test_repo

## Summary:

Retrieve top repo stats from GitHub using GraphQL requests.

## Overview:

This was a fun project. 

I originally wanted to try the classic API call mechanism to Github but found it retrieved too much data with each query. For example, when I used this query: curl https://api.github.com/search/repositories?q=org:twitter, it would retrieve so much more extraneous data than what I needed.

Also, I would have had to use different API endpoints to get stargazers and forks counts on one endpoint and PR counts on another endpoint (with multiple calls to get PR counts for each individual repo). 

I did some digging and it seemed online discussions and by Github's own admission - in their blog post - that this is why some people felt frustrated with the old style REST call mechanisms.

So with that first impasse, I did some more research and found that a more efficient/next generation API calling framework - supported by GitHub - was GraphQL.

After using their online GraphQL I proved it worked out a lot better and the queries I needed to make could be accomplished against one endpoint and with one JSON call.


## Requirements:

This was developed on Python 3. I used Python 3.7 and used some common modules for developing this command line application.

There is a requirements.txt file in the root folder listing some of the required modules.

You can install the modules by running pip: pip3 install -r requirements.txt


## How to run on the command line:

NOTE: You will need to run this with your own created Github access token. I cannot share mine.

If you go to the github directory under the project's root folder, you should be able run an equivalent command as listed below:

./github_query_driver.py organization twitter N 5 token [your token here]

required parameters:

1. organization. Plug your organization name after this parameter. The default is Twitter
2. N the number of top results to return. Must be an integer.
3. Your personal access token to use this tool which will be passed to the GraphQL API endpoint

## TODOS:

There are plenty of TODOS here but further refactoring and cleanup would be advantageous.

Also, if you use an expired token the messaging could be better with a better try/except clause and message to the user.

Additionally, I would fully flesh out the unit tests too since that is pretty minimal right now.

I had to timebox this effort since I have other obligations in my work week.
