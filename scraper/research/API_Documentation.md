---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3 (ipykernel)
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
posts[0]['reactions_counts']
```

```python
#Showing the first post just to display the general structure
users = list(map(lambda x: x['account'], posts))
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
reactions_counts = post['reactions_counts']
account_info = post['account']
account_id = account_info['id']
account_username = account_info['username']
account_name = account_info['acct']
account_is_bot = account_info['bot']
account_display = account_info['display_name']
account_is_verified = account_info['is_verified']
account_created_at = account_info['created_at']
account_note = account_info['note']
```

### Post Utility Functions 

Useful functions pertaining to pulling and processing posts.

```python
def get_posts(n_pages: int, sort_by='hot'):
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
        url = 'https://gab.com/api/v1/timelines/explore?page={}&sort_by={}'.format(page_number, sort_by)
        response = requests.get(url, headers=headers)
        #Decoding the response into a Python list
        posts.extend(json.loads(response.content.decode('utf-8')))
        
    return(posts)
    
```

```python
def unpack_post_data(post: dict[str, any]):
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
    reactions_counts = post['reactions_counts']
    
    return([content, created_at, revised_at, reblogs_count, replies_count, favourites_count, reactions_counts])
```

```python
def get_author_info_from_post(post: dict[str, any]):
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
    account_is_bot = account_info['bot']
    
    return([account_info, account_id, account_username, account_name, account_display, account_is_verified,
           account_created_at, account_note, account_followers, account_is_bot])
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
comments = []
for i in range(1,16):
    url = 'https://gab.com/api/v1/comments/{}?max_id={}'.format(posts[1]['id'],i)
    response = requests.get(url, headers=headers)
    comments.extend(json.loads(response.content.decode('utf-8')))
    

```

```python
len(set(list(map(lambda x: x['id'], comments))))
```

Based on some experimentation here, it seems like the way to get all of the replies to a given post (or comment) is to gather everything for a given post id up to a max_id (in the URL parameter max_id) of (floor($\frac{replies\_count}{10}$) + 1)


## Comment Utility Functions

```python
import math
def get_post_comments(post: dict[str, any]) -> list[dict]:
    '''
    Description: Gets all comments from a post in a nested structure
    
    Input: 
        post (dict): a single gab post
        
    Output:
        comments (list of dicts): A list of comment objects structured {'comment': comment, 'replies': replies}
            where comment is the actual comment object returned by the API and replies is a list of
            comments in reply to this one. This preserves the hierarchical structure of conversations.
    '''
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
    }
    post_id = post['id']
    post_replies_count = post['direct_replies_count']
    if post_replies_count == 0:
        return []
    max_ids = math.floor(post_replies_count/10) + 1
    comments = []
    for max_id in range(max_ids):
        url = 'https://gab.com/api/v1/comments/{}?max_id={}'.format(post_id,max_id)
        response = requests.get(url, headers=headers)
        comments.extend(json.loads(response.content.decode('utf-8')))
    
    comment_tree = []
    for comment in comments:
        comment_tree.append({'comment':comment, 'replies':get_subcomments(comment)})
        
    return comment_tree
    
def get_subcomments(comment: dict[str, any]) -> list[dict]:
    '''
    Description: Gets all subcomments from a comment in a nested structure, really intended only to be called by
        get_post_comments
    
    Input: 
        comment (dict): a single comment post
        
    Output:
        comment_tree (list of dicts): A list of comment objects structured {'comment': comment, 'replies': replies}
            where comment is the actual comment object returned by the API and replies is a list of
            comments in reply to this one. This preserves the hierarchical structure of conversations.
    '''
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
    }
    #gab returns a key-value {'error':'Record not found'} if a comment was deleted, this handles that case
    if 'error' in comment:
        return []
    comment_id = comment['id']
    comment_replies_count = comment['direct_replies_count']
    if comment_replies_count == 0:
        return []
    max_ids = math.floor(comment_replies_count/10) + 1
    child_comments = []
    for max_id in range(max_ids):
        url = 'https://gab.com/api/v1/comments/{}?max_id={}'.format(comment_id,max_id)
        response = requests.get(url, headers=headers)
        child_comments.extend(json.loads(response.content.decode('utf-8')))
    
    child_tree = []
    for child_comment in child_comments:
        child_tree.append({'comment':child_comment, 'replies':get_subcomments(child_comment)})
        
    return child_tree
```

<!-- #raw -->
def get_replies(comments):
    if (comments == []):
        return []
    else:
        #Getting a list of all lists of replies
        replies = [comment['replies'] for comment in comments]
        #Flattening the list of lists of replies into just a list of replies
        replies = [item for sublist in replies for item in sublist]
        #Recursively calling funcion on every item
        replies = get_replies(replies)
        return [*comments, *replies]
<!-- #endraw -->

```python
def get_replies(comments: list):
    if (comments == []):
        return []
    else:
        replies = [comment['replies'] for comment in comments]
        replies = [item for sublist in replies for item in sublist]
        return [*comments, *get_replies(replies)]
    
def remove_duplicate_comments(flat_comments: list):
    comment_ids = list(set([comment['id'] for comment in flat_comments]))
    #Keeping track of which comment ids already appear in the reduced list
    id_used = {comment_id: False for comment_id in comment_ids}
    reduced_comments = []
    for comment in flat_comments:
        if (id_used[comment['id']] == False):
            reduced_comments.append(comment)
            id_used[comment['id']] = True
        else:
            pass
    return reduced_comments
```

```python
post = posts[0]
comment_tree = get_post_comments(post)
```

```python
#Getting all comment replies and flattening them
flat_comments = get_replies(comment_tree)
#Extracting comments down to their base form from the API
flat_comments = [comment['comment'] for comment in flat_comments]
#Removing comments that failed to load (possibly were deleted)
flat_comments = [comment for comment in flat_comments if comment != 'error']
#Removing redundant duplicate comments
reduced_comments = remove_duplicate_comments(flat_comments)
```

```python
users = [comment['account'] for comment in reduced_comments]
```
