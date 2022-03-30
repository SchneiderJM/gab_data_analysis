---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Gab API

Here, the Gab API is documented. Mostly in terms of how to pull information that I find useful.


### Posts

Using API calls to pull and extract the necessary information from it

```python
import requests
import json

#This url pulls the front page, the page number can be changed to grab more posts
url = 'https://gab.com/api/v1/timelines/explore?page=1&sort_by=hot'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}
response = requests.get(url, headers=headers)
#Decoding the response into a Python list
posts = json.loads(response.content.decode('utf-8'))
```

```python
#Lists attributes usable 
dir(posts[0])
```

```python

```
