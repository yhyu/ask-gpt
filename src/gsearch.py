import os
import requests
import backoff
from local_cache import MemoryCache

api_url = os.environ.get(
    'SEARCH_ENGINE_URL',
    default='https://customsearch.googleapis.com/customsearch/v1',
)
api_key = os.environ['SEARCH_ENGINE_API_KEY']
engine_id = os.environ['SEARCH_ENGINE_ID']

def backoff_hdlr(details):
    print("[Search] Backing off {wait:0.1f} seconds after {tries} tries "
          "calling function {target} with args {args} and kwargs "
          "{kwargs}".format(**details))


@backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout),
        max_time=5,
        on_backoff=backoff_hdlr
    )
@MemoryCache.cache
def get_relevant_pages(q: str, n: int = 1) -> list:
    search_param = {
        'cx': engine_id,
        'key': api_key,
        'q': q,
        'num': n,
    }
    response = requests.get(api_url, search_param)
    print(response.json())
    links = []
    summaries = []
    for item in response.json().get('items', []):
        l = item.get('formattedUrl', '')
        if len(l) > 0:
            links.append(l)
            summaries.append(item.get('snippet', ''))
    return links, summaries
