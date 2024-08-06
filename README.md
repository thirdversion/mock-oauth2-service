[![Continuous integration](https://github.com/strivesolutions/mock-oauth2-service/actions/workflows/ci.yml/badge.svg)](https://github.com/strivesolutions/mock-oauth2-service/actions/workflows/ci.yml)

Forked from [Strive Solutions](https://github.com/strivesolutions/mock-oauth2-service) by the original authors.

# Mock OAuth Server

This is a simple mock OAuth server that can be used for testing purposes.

Never use this in production, it contains no meaningful security. It is intended to mimic a real OAuth server in a local development environment.

There are no user credentials, only a form with a button which emulates a 3rd party auth login.

## Running in Docker

You can run this service in a docker container by pulling the image from the GitHub Container Registry. Images are tagged with a version number, but you can also use `latest` to get the most recent version.

```sh
docker pull ghcr.io/thirdversion/mock-oauth2-service:latest
docker run -p 5000:5000 ghcr.io/thirdversion/mock-oauth2-service:latest
```

### Sample docker-compose:

```yaml
version: "3.9"

services:
  mock-auth:
    image: ghcr.io/thirdversion/mock-oauth2-service:latest
    ports:
      - 5000:5000
    environment:
      - 'ADDITIONAL_CLAIMS={"email": "someuser@nowhere.com", "name": "Some User"}'
```

## Configuration

All configuration is done through environment variables. If running locally, you can create a `.env` file in the root of the project to set these variables.

| Name                               | Type   | Default            | Description                                                                                                                                                               |
| ---------------------------------- | ------ | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PORT`                             | `int`  | `5000`             | The port to run the server on                                                                                                                                             |
| `ACCESS_TOKEN_EXPIRATION_MINUTES`  | `int`  | `30`               | The expiration time for access tokens                                                                                                                                     |
| `REFRESH_TOKEN_EXPIRATION_MINUTES` | `int`  | `180`              | The expiration time for refresh tokens                                                                                                                                    |
| `SUBJECT`                          | `str`  | `mock_user`        | The subject of the token                                                                                                                                                  |
| `ISSUER`                           | `str`  | `DEFAULT_ISSUER`   | The issuer of the token                                                                                                                                                   |
| `AUDIENCE`                         | `str`  | `DEFAULT_AUDIENCE` | The audience of the token                                                                                                                                                 |
| `ADDITIONAL_CLAIMS`                | `json` | `{}`               | A JSON object of additional claims to include in the token, for example, if you want your mock user to have an email claim, you could support {"email": "fake@email.com"} |

## Running in development

This projects uses [Rye](https://rye-up.com) to manage python, dependencies and scripts.

To get started, run `rye sync` to install the dependencies.

Then, run `rye run dev` to start the service.
