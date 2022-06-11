import datetime

def unpack_comment_data(comment: dict[str, any]):
    '''
    Description: Unpacks the data from a comment returning information that I've (somewhat arbitrarily) deemed relevant
    
    Inputs:
        comment (dict): One post returned from the Gab API
        
    Outputs:
        Data relevant to a comment
    '''
    gab_id = comment['id']
    #Turning apostrophes into an escaped version for SQL
    content: str = comment['content'].replace("'", "''")
    in_reply_to_id = comment['in_reply_to_id']
    created_at = datetime.datetime.strptime(comment['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    if comment['revised_at'] != None:
        revised_at = datetime.datetime.strptime(comment['revised_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    else:
        revised_at = 'null'
    reblogs_count = comment['reblogs_count']
    replies_count = comment['replies_count']
    favourites_count = comment['favourites_count']
    
    return([gab_id, in_reply_to_id, content, created_at, revised_at, reblogs_count, replies_count, favourites_count])

def unpack_post_data(post: dict[str, any]):
    '''
    Description: Unpacks the data from a post returning information that I've (somewhat arbitrarily) deemed relevant
    
    Inputs:
        post (dict): One post returned from the Gab API
        
    Outputs:
        Data relevant to a post
    '''
    gab_id = post['id']
    #Turning apostrophes into an escaped version for SQL
    content: str = post['content'].replace("'", "''")
    created_at = datetime.datetime.strptime(post['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    if post['revised_at'] != None:
        revised_at = datetime.datetime.strptime(post['revised_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    else:
        revised_at = 'null'
    reblogs_count = post['reblogs_count']
    replies_count = post['replies_count']
    favourites_count = post['favourites_count']
    reactions_counts = str(post['reactions_counts']).replace('\'','"')
    
    return([gab_id, content, created_at, revised_at, reblogs_count, replies_count, favourites_count, reactions_counts])
	
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
    account_created_at = datetime.datetime.strptime(account_info['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    account_note = account_info['note']
    account_followers = account_info['followers_count']
    account_is_bot = account_info['bot']
    account_is_donor = account_info['is_donor']
    
    return([account_info, account_id, account_username, account_name, account_display, account_is_verified,
           account_created_at, account_note, account_followers, account_is_bot, account_is_donor])

def get_author_info_from_user(account_info: dict[str, any]):
    '''
    Description: Gets the author information from a post
    
    Inputs:
        account_info (dict): One author from the gab API, extracted either from a post or comment
        
    Outputs:
        Author information
    '''
    account_id = account_info['id']
    account_username = account_info['username']
    account_name = account_info['acct']
    account_display = account_info['display_name']
    account_is_verified = account_info['is_verified']
    account_created_at = datetime.datetime.strptime(account_info['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    account_note = account_info['note']
    account_followers = account_info['followers_count']
    account_is_bot = account_info['bot']
    account_is_donor = account_info['is_donor']
    
    return([account_id, account_username, account_name, account_display, account_is_verified,
           account_created_at, account_note, account_followers, account_is_bot, account_is_donor])

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

def get_flattened_comments(comment_tree:list):
    #Getting all comment replies and flattening them
    flat_comments = get_replies(comment_tree)
    #Extracting comments down to their base form from the API
    flat_comments = [comment['comment'] for comment in flat_comments]
    #Removing comments that failed to load (possibly were deleted)
    flat_comments = [comment for comment in flat_comments if comment != 'error']
    #Removing redundant duplicate comments
    reduced_comments = remove_duplicate_comments(flat_comments)

    return reduced_comments