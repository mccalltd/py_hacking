"""Demo use of github module.
"""

import github as gh
from pprint import pprint


separator = '-' * 80

print('\nInfo for mccalltd:\n', separator, sep='')
user = gh.get_user('mccalltd')
pprint({'name': user['name'],
        'followers': user['followers']})

print('\nRepos for mccalltd:\n', separator, sep='')
for r in gh.get_repos('mccalltd'):
    pprint({'name': r['name'],
            'description': r['description']})

print('\nOpen pull requests for rails/rails:\n', separator, sep='')
for r in gh.get_pull_requests('rails', 'rails'):
    pprint({'body': r['body'],
            'submitter': r['user']['login'],
            'commit_id': r['head']['sha']})
