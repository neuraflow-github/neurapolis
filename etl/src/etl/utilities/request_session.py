import requests


def create_request_session() -> requests.Session:
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        max_retries=requests.adapters.Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


request_session = create_request_session()
