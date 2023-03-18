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
```
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
export SEARCH_ENGINE_API_KEY=<YOUR_GOOGLE_SEARCH_API_KEY>
export SEARCH_ENGINE_ID=<YOUR_GOOGLE_SEARCH_ENGINE_ID>
```
4. Other optional settings. Here are default settings.
```
export LLM_COMPLETION_MODEL=text-davinci-003
export SEARCH_ENGINE_URL=https://customsearch.googleapis.com/customsearch/v1
```
