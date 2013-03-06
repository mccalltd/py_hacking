"""GitHub API v3 wrapper.

General usage:
    For funtions returning a single result, the result is returned directly.
    For functions returning multiple results, one of two things happen:
        - If no callback is given:  returns an iterable over the results;
        - If a callback is given:   the results are yielded to the callback; returns None.

TODO: doctest
"""

from urllib.request import urlopen, Request
import gzip
import json


def get_pull_requests(owner, repo, callback=None):
    """Gets the pull requests for the given repository.

    owner: ''           The name of the repository owner.
    repo: ''            The name of the repository.
    callback: f(i)      Do something with each item (eg: print is a pretty handy callback);
                        by default each item is yielded.
    """

    path = '/repos/{0}/{1}/pulls'.format(owner, repo)
    response = get_response(path)
    return yield_to_callback(response, callback)


def get_repos(user, callback=None):
    """Gets the repositories for the given user.

    user: ''            The name of the user.
    callback: f(i)      Do something with each item (eg: print is a pretty handy callback);
                        by default each item is yielded.
    """

    path = '/users/{0}/repos'.format(user)
    response = get_response(path)
    return yield_to_callback(response, callback)


def get_response(path, set_root=None):
    """Generator function for iterating over JSON response data.

    path: ''            The path to the github API resource.
    set_root: f(r)      Navigates to a position on the object graph before yielding;
                        by default the root is the complete json object.
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
    data_root = set_root(json_data) if set_root else json_data

    # If the data root is not a list, wrap it so we can have one yield via the iterator.
    if not isinstance(data_root, list):
        data_root = [data_root]

    # Iterate and yield mapped data to the caller.
    for data in data_root:
        yield data


def get_user(user):
    """Gets info for the user.

    user: ''            The name of the user.
    """

    path = '/users/' + user
    response = get_response(path)
    return next(response)


def search_repos(keyword, callback=None):
    """Finds repositories matching the given keyword.

    keyword: ''         The keyword to search with.
    callback: f(i)      Do something with each item (eg: print is a pretty handy callback);
                        by default each item is yielded.
    """

    path = '/legacy/repos/search/' + keyword
    response = get_response(path, set_root=lambda r: r['repositories'])
    return yield_to_callback(response, callback)


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
