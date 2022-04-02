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


## Posts

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
#Showing the first post just to display the general structure
posts[0]
```

```python
#Getting relevant information from the first post
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

### Post Utility Functions 

Useful functions pertaining to pulling and processing posts.

```python
def get_posts(n_pages, sort_by='hot'):
    '''
    Description: Gets posts from the Gab API
    
    Inputs:
        n_pages (int): Number of pages of posts to get, each page contains 10 posts
        sort_by (string): Sorting method, defaults to "hot" just like the website itself
        
    Outputs:
        posts (list): List of posts returned by API
    '''
    #Sets User-Agent to something the API supports
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
    }
    posts = []
    for page_number in range(n_pages):
        url = 'https://gab.com/api/v1/timelines/explore?page={}&sort_by={}}'.format(page_number, sort_by)
        response = requests.get(url, headers=headers)
        #Decoding the response into a Python list
        posts.extend(json.loads(response.content.decode('utf-8')))
        
    return(posts)
    
```

```python
def unpack_post_data(post):
    '''
    Description: Unpacks the data from a post returning information that I've (somewhat arbitrarily) deemed relevant
    
    Inputs:
        post (dict): One post returned from the Gab API
        
    Outputs:
        Data relevant to a post
    '''
    content = post['content']
    created_at = post['created_at']
    revised_at = post['revised_at']
    reblogs_count = post['reblogs_count']
    replies_count = post['replies_count']
    favourites_count = post['favourites_count']
    
    return([content, created_at, revised_at, reblogs_count, replies_count, favourites_count])
```

```python
def get_author_info_from_post(post):
    '''
    Description: Gets the author information from a post
    
    Inputs:
        post (dict): One post returned from the Gab API
        
    Outputs:
        Author information
    '''
    account_info = post['account']
    account_id = account_info['id']
    account_username = account_info['username']
    account_name = account_info['acct']
    account_display = account_info['display_name']
    account_is_verified = account_info['is_verified']
    account_created_at = account_info['created_at']
    account_note = account_info['note']
    account_followers = account_info['followers_count']
    
    return([account_info, account_id, account_username, account_name, account_display, account_is_verified,
           account_created_at, account_note, account_followers])
```

## Comments

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

Note you can also use a comment ID instead of a post ID to get the replies to a comment.

```python
url = 'https://gab.com/api/v1/comments/{}?max_id={}'.format(posts[0]['id'],10)#?max_id=1&sort_by=most-liked'.format(posts[0]['id'])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}
response = requests.get(url, headers=headers)
#Decoding the response into a Python list
comments = json.loads(response.content.decode('utf-8'))
```

```python
posts[2]['replies_count']
```

```python
comments = []
for i in range(20):
    url = 'https://gab.com/api/v1/comments/{}?max_id={}'.format(posts[2]['id'],i)
    response = requests.get(url, headers=headers)
    comments.append(json.loads(response.content.decode('utf-8')))
    

```

```python
comment = comments[0][0]
comment
```

```python
url = 'https://gab.com/api/v1/comments/{}?max_id={}'.format('108061787025501269',10)#?max_id=1&sort_by=most-liked'.format(posts[0]['id'])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}
response = requests.get(url, headers=headers)
#Decoding the response into a Python list
comments = json.loads(response.content.decode('utf-8'))
```

```python
len(comments)
```
