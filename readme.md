# Swagger Django Validator

Github Action to Validate the correctness of a Swagger file for Django apps.

The following checks are performed:
- Django endpoints not registered in the Swagger file.
- Swagger endpoints that are unresolvable to any Django endpoints.

This action only matches endpoints. It does not validate parameters, headers, or even method types.


#### Usage

Add the following workflow to your repository to use this Github Action:


```yml
on: [pull_request]

jobs:
  swagger-django-validator:
    runs-on: ubuntu-latest
    name: Swagger Django Validator
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0
      - name: swagger-django-validator
        id: swagger-django-validator
        uses: rohithpr/swagger-django-validator@master
        env:
          SWAGGER_FILE_PATH: path/to/file.yml  # Relative path to the swagger file being checked.
          DJANGO_SETTINGS_MODULE: path.to.file  # Dot separated path to the project's settings file.
          IGNORE_SWAGGER_PATTERNS: "pattern_to_ignore,pattern_to_ignore"  # Optional, comma separated list of patterns to be ignored in the swagger file.
          IGNORE_DJANGO_PATTERNS: "pattern_to_ignore,pattern_to_ignore"  # Optional, comma separated list of patterns to be ignored in the Django app.
```

## Improvements to be made

- Validate that all method types are registered correctly.
- Validate parameters (at least for DRF).
- Validate input and outputs for JSON-API.
