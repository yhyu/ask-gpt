import requests
from urllib.parse import urlparse, urljoin
from local_cache import MemoryCache
import backoff

wiki_endpoint = '/w/api.php'

# Referenced from https://pypi.org/project/backoff/
def backoff_hdlr(details):
    print("[Wiki] Backing off {wait:0.1f} seconds after {tries} tries "
          "calling function {target} with args {args} and kwargs "
          "{kwargs}".format(**details))


@backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout),
        max_time=5,
        on_backoff=backoff_hdlr
    )
@MemoryCache.cache
def get_abstract(url: str) -> str:
    url_elements = urlparse(url)
    title = url_elements.path.split('/')[-1]
    api_url = urljoin(url, wiki_endpoint)
    api_params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
        'titles': title
    }
    response = requests.get(api_url, params=api_params)
    if response.status_code == 200:
        page = next(iter(response.json()['query']['pages'].values()))
        return page.get('extract', '')
    else:
        return ''
