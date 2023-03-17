import os
from pathlib import Path
from joblib import Memory

cache_loc = os.environ.get(
    'ASKGPT_CACHE_LOC',
    default=os.path.join(Path.home(), 'cache_askGPT')
)
MemoryCache = Memory(location=cache_loc, verbose=0)
