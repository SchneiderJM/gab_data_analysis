import math
import requests
import json

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