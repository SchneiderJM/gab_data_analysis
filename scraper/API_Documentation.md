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
posts[0]
```

```python
#Getting relevant information from the post
post = posts[0]
content = post['content']
created_at = post['created_at']
revised_at = post['revised_at']
reblogs_count = post['reblogs_count']
replies_count = post['replies_count']
favourites_count = post['favourites_count']
account_info = post['account']
account_id = account_info['id']
account_username = account_info['username']
account_name = account_info['acct']
account_display = account_info['display_name']
account_is_verified = account_info['is_verified']
account_created_at = account_info['created_at']
account_note = account_info['note']
```

```python

```
