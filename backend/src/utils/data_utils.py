import datetime
def unpack_post_data(post: dict[str, any]):
    '''
    Description: Unpacks the data from a post returning information that I've (somewhat arbitrarily) deemed relevant
    
    Inputs:
        post (dict): One post returned from the Gab API
        
    Outputs:
        Data relevant to a post
    '''
    gab_id = post['id']
    content = post['content']
    created_at = datetime.datetime.strptime(post['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    revised_at = datetime.datetime.strptime(post['revised_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    reblogs_count = post['reblogs_count']
    replies_count = post['replies_count']
    favourites_count = post['favourites_count']
    reactions_counts = post['reactions_counts']
    
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