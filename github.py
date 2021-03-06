"""GitHub API v3 wrapper.

TODO: doctest
"""

from urllib.request import urlopen, Request
import gzip
import json


def get(path):
    """Returns the JSON response data from the requested path.
    :path   The path to the github API resource.
    """
    request = Request('https://api.github.com/' + path.lstrip('/'))
    request.add_header('Accept-Encoding', 'gzip')

    with urlopen(request) as response:
        raw = response.read()
        response_body = gzip.decompress(raw).decode()

    return json.loads(response_body)


def get_pull_requests(owner, repo):
    """Gets the pull requests for the given repository.
    :owner  The name of the repository owner.
    :repo   The name of the repository.
    """
    return get('/repos/{0}/{1}/pulls'.format(owner, repo))


def get_repos(user):
    """Gets the repositories for the given user.
    :user   The name of the user.
    """
    return get('/users/{0}/repos'.format(user))


def get_user(user):
    """Gets info for the user.
    :user   The name of the user.
    """
    return get('/users/' + user)


def search_repos(keyword):
    """Finds repositories matching the given keyword.
    :keyword    The keyword to search with.
    """
    return get('/legacy/repos/search/' + keyword)['repositories']
