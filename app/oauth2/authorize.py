def create_authorization_form(client_id: str, redirect_uri: str, scope: str, response_type: str, code_challenge: str | None, code_challenge_method: str | None) -> str:
    content = f"""
 <html>
        <head>
            <title>Authorize</title>
            <style>
                form {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                }}
                button {{
                    padding: 10px 20px;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <form action="/authorize" method="post">
            <h1>Mock OAuth Server</h1>
                <input type="hidden" name="client_id" value="{client_id}">
                <input type="hidden" name="redirect_uri" value="{redirect_uri}">
                <input type="hidden" name="scope" value="{scope}">
                <input type="hidden" name="response_type" value="{response_type}">
                <input type="hidden" name="code_challenge" value="{code_challenge}">
                <input type="hidden" name="code_challenge_method" value="{code_challenge_method}">
                <button type="submit">Authorize</button>
            <h3>Do not use in production!</h3>
            </form>
        </body>
    </html>
    """
    return content
