# ask-gpt
Integrate IR and LLM to improve question answering accuracy.

## Architecture
![](https://github.com/yhyu/ask-gpt/blob/main/resources/images/architecture.jpg)

## Prerequisites
### Install requirements:
```
pip3 install --no-cache-dir -r requirements.txt
```

### Prepare LLM and IR  
1. Prepare [OpenAI API kay](https://platform.openai.com/account/api-keys).  
2. Create [google programmable search engine](https://programmablesearchengine.google.com/controlpanel/create).  
3. Export following api keys.
```console
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
export SEARCH_ENGINE_API_KEY=<YOUR_GOOGLE_SEARCH_API_KEY>
export SEARCH_ENGINE_ID=<YOUR_GOOGLE_SEARCH_ENGINE_ID>
```
4. Other optional settings. Here are default settings.
```console
export LLM_COMPLETION_MODEL=text-davinci-003
export SEARCH_ENGINE_URL=https://customsearch.googleapis.com/customsearch/v1
```

## Examples
```console
$ cd src
$ python askme.py -q "Is the current speaker of the U.S. House of Representatives the same political party as the current U.S. president?"
Answer: No
Reason: The current speaker of the U.S. House of Representatives is a Republican, while the current U.S. president is a Democrat.
$
$ python askme.py -q "誰是現任台北市長的父親?"
Answer: 蔣孝嚴
Reason: 蔣萬安的父親為蔣孝嚴。
$
$ python askme.py -q "A bank headquartered in Santa Clara, California has recently failed. In what year was this bank founded?"
Answer: 1983
Reason: Silicon Valley Bank was founded in 1983.
$
```
