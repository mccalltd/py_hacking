from urllib.request import urlopen
import json
from pprint import pprint

with urlopen('https://api.github.com/repos/rails/rails/pulls') as response:
    response_body = response.read().decode()

for i in json.loads(response_body):
    pprint({'body': i['body'],
            'user': i['user']['login'],
            'commit_id': i['head']['sha']})
