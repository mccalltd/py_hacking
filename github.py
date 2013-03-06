"""Get data from the GitHub API v3.

General usage:
    For funtions returning a single result, that result is returned directly.
    For functions returning multiple results, one of two things happen:
        - If no callback is given:  returns an iterable over the results;
        - If a callback is given:   the results are yielded to the callback; returns None.
"""

from urllib.request import urlopen, Request
import gzip
import json


def find_repos(keyword, callback=None):
    """Print repositories matching the given keyword.

    keyword: ''         The keyword to search with.
    callback: f(item)   Do something with each item (eg: print is a pretty handy callback);
                        by default each item is yielded.
    """

    path = '/legacy/repos/search/' + keyword
    set_data_root = lambda root: root['repositories']
    data_map = lambda data: {'type': data['type'],
                             'name': data['owner'] + ':' + data['name'],
                             'score': data['score'],
                             'description': data['description'],
                             'followers': data['followers'],
                             'forks': data['forks']}

    return yield_to_callback(response_json(path, data_map, set_data_root), callback)


def get_pull_requests(owner, repo, callback=None):
    """Yields the pull requests for the given repository.

    owner: ''           The name of the repository owner.
    repo: ''            The name of the repository.
    callback: f(item)   Do something with each item (eg: print is a pretty handy callback);
                        by default each item is yielded.
    """

    path = '/repos/{0}/{1}/pulls'.format(owner, repo)
    data_map = lambda data: {'user': data['user']['login'],
                             'commit': data['head']['sha'],
                             'body': data['body']}

    return yield_to_callback(response_json(path, data_map), callback)


def get_repos(user, callback=None):
    """Yields the repositories for the given user.

    user: ''            The name of the user.
    callback: f(item)   Do something with each item (eg: print is a pretty handy callback);
                        by default each item is yielded.
    """

    path = '/users/{0}/repos'.format(user)
    data_map = lambda data: {'name': data['name'],
                             'homepage': data['homepage'],
                             'watchers': data['watchers'],
                             'forks': data['forks'],
                             'open_issues': data['open_issues']}

    return yield_to_callback(response_json(path, data_map), callback)


def get_user(user):
    """Returns info for the user.

    user: ''    The name of the user.
    """

    path = '/users/' + user
    data_map = lambda data: {'login': data['login'],
                             'name': data['name'],
                             'company': data['company'],
                             'bio': data['bio'],
                             'email': data['email'],
                             'blog': data['blog']}

    return next(response_json(path, data_map))


def response_json(path, data_map=lambda d: d, set_root=lambda r: r):
    """Generator for iterating over JSON response data.

    path: ''            The path to the github API resource.
    data_map: f(data)   Maps the data from one form to another;
                        by default it returns the original json object.
    set_root: f(root)   Navigates to a position on the object graph before yielding;
                        by default it returns the complete json object.
    """

    # Set up request object
    request = Request('https://api.github.com/' + path.lstrip('/'))
    request.add_header('Accept', 'application/json;charset=utf-8')
    request.add_header('Accept-Encoding', 'gzip')

    # Get the decompressed response
    response = None
    with urlopen(request) as f:
        response = gzip.decompress(f.read())

    # Parse JSON data and adjust the root of the object graph.
    json_data = json.loads(response.decode())
    data_root = set_root(json_data)

    # If the data root is not a list, wrap it so we can have one yield via the iterator.
    if not isinstance(data_root, list):
        data_root = [data_root]

    # Iterate and yield mapped data the caller.
    for data in data_root:
        yield data_map(data)


def yield_to_callback(iterable, callback):
    """Returns the iterable if no callback is given; otherwise iterates and passes items to callback.

    iterable: iterable
    callback: f()
    """

    if callback:
        for item in iterable:
            callback(item)
    else:
        return iterable
