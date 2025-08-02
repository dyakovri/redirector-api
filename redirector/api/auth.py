from fastapi_auth_oidc import OIDCProvider, IDToken
from redirector.settings import get_settings

settings = get_settings()
auth_user = OIDCProvider(
    configuration_uri=str(settings.oidc_configuration_uri),
    client_id=settings.oidc_client_id,
    token_type=IDToken,
)
