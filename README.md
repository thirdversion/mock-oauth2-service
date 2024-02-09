# Mock OAuth Server

This is a simple mock OAuth server that can be used for testing purposes.

Never use this in production, it contains no meaningful security. It is intended to mimic a real OAuth server in a local development environment.

There are no user credentials, only a form which mimics the OAuth flow. As of now, this server only supports the code exchange flow.

## Usage

This projects uses [Rye](https://rye-up.com) to manage python, dependencies and scripts.

To get started, run `rye sync` to install the dependencies.

Then, run `rye run dev` to start the service.

## Environment Variables

The following environment variables are available, but optional.

- `PORT` - The port to run the server on. Defaults to `5000`.
- `ACCESS_TOKEN_EXPIRATION_MINUTES` - The expiration time for access tokens. Defaults to `30`.
- `REFRESH_TOKEN_EXPIRATION_MINUTES` - The expiration time for refresh tokens. Defaults to `180`.
- `SUBJECT` - The subject of the token. Defaults to `mock_user`.
- `ISSUER` - The issuer of the token. Defaults to `DEFAULT_ISSUER`.
- `AUDIENCE` - The audience of the token. Defaults to `DEFAULT_AUDIENCE`.
- `ADDITIONAL_CLAIMS` - A JSON object of additional claims to include in the token. Defaults to `{}`.
