import os
import openai
import openai.error
import backoff
from local_cache import MemoryCache

default_openai_model = os.environ.get('LLM_COMPLETION_MODEL', 'text-davinci-003')
default_openai_api_key = os.environ['OPENAI_API_KEY']


# Referenced from https://pypi.org/project/backoff/
def backoff_hdlr(details):
    print("[GPT] Backing off {wait:0.1f} seconds after {tries} tries "
          "calling function {target} with args {args} and kwargs "
          "{kwargs}".format(**details))


class GPT():
    def __init__(
            self, model: str = default_openai_model,
            api_key: str = default_openai_api_key,
            max_tokens: int = 4096) -> None:
        if api_key:
            openai.api_key = api_key

        self.max_tokens = max_tokens

        self.parameters = {
            'model': model,
            'temperature': 0.,
            'top_p': 1,
            'max_tokens': 1024,  # prompt + completion <= 4096
            'n': 1,
            'frequency_penalty': 0,
            'presence_penalty': 0,
        }

    @backoff.on_exception(
            backoff.expo,
            (openai.error.RateLimitError,
             openai.error.ServiceUnavailableError),
            max_time=5,
            on_backoff=backoff_hdlr
        )
    def __call__(self, prompt: str, **kwds):
        if self.max_tokens - len(prompt) <= 0:
            print('token is too long...')
            return {}
        return self.complete(prompt, **kwds)

    def complete(self, prompt: str, **kwds):
        req_param = {
            **self.parameters,
            'prompt': prompt,
            'max_tokens': self.max_tokens - len(prompt),
            **kwds,
        }
        response = request_gpt(**req_param)

        answers = []
        for c in response['choices']:
            single_answer = {}
            for item in c['text'].split('\n'):
                kv = item.split(': ')
                if len(kv) == 2:
                    single_answer[kv[0]] = kv[1]
            answers.append(single_answer)
        return answers


@MemoryCache.cache
def request_gpt(**req_param):
    return openai.Completion.create(**req_param)
