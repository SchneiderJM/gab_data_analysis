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

Using API calls to pull and extract information from posts.

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
print(replies_count)
```

### Comments

Using API calls to pull and extract information from comments.

```python
url = 'https://gab.com/api/v1/comments/{}'.format(posts[0]['id'])#?max_id=1&sort_by=most-liked'.format(posts[0]['id'])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}
response = requests.get(url, headers=headers)
#Decoding the response into a Python list
comments = json.loads(response.content.decode('utf-8'))
```

The url uses a consistent format to pull comments, it seems to be along the lines of:

https://gab.com/api/v1/comments/[post_id]
to pull comments, though it can take a "sort_by" argument (thus allowing you to sort it according to how people on the site will see it by default) and a max_id argument. If you don't use max_id (or if you set max_id <= 1) you will only get the first ten comments. In order to get the rest, you will need to keep re-running the query with a new max_id value. It appears that incrementing max_id by one (eg going from max_id = 1 to max_id = 2) will get the next ten comments. You should be able to use the "replies_count" from the post in order to determine how many times max_id will need to be incremented in order to get all of the comments.
