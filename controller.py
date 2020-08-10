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


def main():
    resolver = get_resolver()
    swagger_file_path = get_env_var("SWAGGER_FILE_PATH")
    swagger_contents = read_swagger_file(swagger_file_path)
    swagger_endpoints = get_swagger_endpoints(swagger_contents)
    unresolvable_swagger_endpoints = get_unresolvable_endpoints(
        resolver, swagger_endpoints
    )


if __name__ == "__main__":
    main()
