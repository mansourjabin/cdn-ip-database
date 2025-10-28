import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_TIMEOUT_SECONDS = 10

USER_AGENT = (
    "cdn-ip-database-bot/1.0 (+https://github.com/mansourjabin/cdn-ip-database)"
)


def _get_retry_strategy() -> Retry:
    return Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
        respect_retry_after_header=True,
    )


def get_session() -> requests.Session:
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=_get_retry_strategy())
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def fetch(session: requests.Session, url: str) -> requests.Response:
    return session.get(url, timeout=DEFAULT_TIMEOUT_SECONDS)
