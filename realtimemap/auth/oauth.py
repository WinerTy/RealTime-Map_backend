from httpx_oauth.clients.google import GoogleOAuth2

from core.config import conf

if conf.api.v1.auth.activate_google_auth:
    google_oauth_client = GoogleOAuth2(
        conf.api.v1.auth.google_client_id,
        conf.api.v1.auth.google_client_secret,
    )
