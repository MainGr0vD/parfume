from tapi_yandex_market import YandexMarket

OAUTH_TOKEN = "{oauth_token}"
OAUTH_CLIENT_ID = "{oauth_client_id}"

client = YandexMarket(
    # https://yandex.ru/dev/market/partner/doc/dg/concepts/authorization.html
    oauth_token=OAUTH_TOKEN,
    oauth_client_id=OAUTH_CLIENT_ID,
    # Will retry the request if the request limit is reached.
    retry_if_exceeded_requests_limit=True,
)