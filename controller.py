import os

import django
import yaml
from django.urls import URLPattern, URLResolver, get_resolver
from django.urls.exceptions import Resolver404

django.setup()


def get_env_var(var_name):
    env_var = os.environ.get(var_name)
    if not env_var:
        raise Exception(f"Environment variable `{var_name}` not found.")
    return env_var


def read_swagger_file(file_path):
    with open(file_path) as fp:
        contents = yaml.safe_load(fp)
    return contents


def get_swagger_endpoints(file_contents):
    return file_contents["paths"].keys()


def get_clean_django_endpoint(parts):
    """Turn a list of path parts into a clean path.

    Example: ["^", "^login/$"] -> /login/
    """
    path = ""
    for part in parts:
        part = part.lstrip("^").rstrip("$")
        # TODO: Can this be replaced with anything but an empty string?
        part = part.replace("\\.(?P<format>[a-z0-9]+)/?", "")
        part = part.replace("(?P<pk>[^/.]+)", "1")
        if part:
            path = "/".join((path, part))
    path = path.replace("//", "/")
    return path


def get_django_endpoints(url_patterns):
    def list_urls(lis, acc=None):
        # https://stackoverflow.com/a/54531546
        # TODO: Clean up and move this out.
        if acc is None:
            acc = []
        if not lis:
            return
        l = lis[0]
        if isinstance(l, URLPattern):
            yield acc + [str(l.pattern)]
        elif isinstance(l, URLResolver):
            yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
        yield from list_urls(lis[1:], acc)

    endpoints = []
    for path_parts in list_urls(url_patterns):
        endpoint = get_clean_django_endpoint(path_parts)
        endpoints.append(endpoint)
    return endpoints


def get_unresolvable_endpoints(resolver, endpoints):
    unresolvable_endpoints = []
    for endpoint in endpoints:
        try:
            # Note: This isn't really a perfect way of doing what we wish to do here.
            # /domain/resource in a swagger file could end up matching /domain/{id}, for instance.
            # However, it's good enough for current use cases.
            _ = resolver.resolve(endpoint)
        except Resolver404:
            unresolvable_endpoints.append(endpoint)
    return unresolvable_endpoints


def get_resolvable_swagger_endpoints(resolver, *, log_unresolvable_paths=True):
    file_path = get_env_var("SWAGGER_FILE_PATH")
    file_contents = read_swagger_file(file_path)
    endpoints = get_swagger_endpoints(file_contents)
    unresolvable_endpoints = get_unresolvable_endpoints(resolver, endpoints)
    resolvable_endpoints = set(endpoints) - set(unresolvable_endpoints)
    if log_unresolvable_paths:
        print(f"Found the following unresolvable endpoints in the Swagger file: {unresolvable_endpoints}")
    return resolvable_endpoints, bool(unresolvable_endpoints)


def get_resolvable_django_endpoints(resolver, *, log_unresolvable_paths=True):
    endpoints = get_django_endpoints(resolver.url_patterns)
    # TODO: Refactor
    unresolvable_endpoints = get_unresolvable_endpoints(endpoints)
    resolvable_endpoints = set(endpoints) - set(unresolvable_endpoints)
    if log_unresolvable_paths:
        print(f"Found the following unresolvable endpoints in the Django app: {unresolvable_endpoints}")
        print(
            "This shouldn't happen, and is likely to be an issue with the validation tool. Please report the issue to the maintainer of the project."
        )
    return resolvable_endpoints, bool(unresolvable_endpoints)


def main():
    resolver = get_resolver()
    resolvable_swagger_endpoints, swagger_has_unresolvable_endpoints = get_resolvable_swagger_endpoints(resolver)
    resolvable_django_endpoints, django_has_unresolvable_endpoints = get_resolvable_django_endpoints(resolver)


if __name__ == "__main__":
    main()
