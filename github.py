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
    # Set up the request object.
    request = Request('https://api.github.com/' + path.lstrip('/'))
    request.add_header('Accept', 'application/json;charset=utf-8')
    request.add_header('Accept-Encoding', 'gzip')

    # Get the decompressed response.
    response = None
    with urlopen(request) as f:
        response = gzip.decompress(f.read())

    # Parse and return JSON data.
    return json.loads(response.decode())


def get_pull_requests(owner, repo):
    """Gets the pull requests for the given repository.
    :owner  The name of the repository owner.
    :repo   The name of the repository.
    """
    return get('/repos/%s/%s/pulls' % owner, repo)


def get_repos(user):
    """Gets the repositories for the given user.
    :user   The name of the user.
    """
    return get('/users/%s/repos' % user)


def get_user(user):
    """Gets info for the user.
    :user   The name of the user.
    """
    return get('/users/%s' % user)


def search_repos(keyword, callback=None):
    """Finds repositories matching the given keyword.
    :keyword    The keyword to search with.
    """
    return get('/legacy/repos/search/%s' % keyword)['repositories']
