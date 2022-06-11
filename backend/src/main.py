from fastapi import FastAPI
import utils.scraper_utils as su
import utils.database_utils as dbutils
import utils.data_utils as datautils

app = FastAPI()

@app.get('/archive_latest_posts')
async def archive_latest_posts():
	print('starting')
	posts = su.get_posts(1)
	#Grabbing the first five posts just for test purposes
	posts = posts[0:1]
	users = list(map(lambda x: x['account'], posts))
	dbutils.write_users(users)
	dbutils.write_posts(posts)
	#Collecting and writing comments for each post individually since they're quite large
	#and take a long time to gather/write
	for post in posts:
		print('getting comments')
		comment_tree = su.get_post_comments(post)
		print('got comments')
		flat_comments = datautils.get_flattened_comments(comment_tree)
		comment_users = [comment['account'] for comment in flat_comments]
		print('writing users')
		dbutils.write_users(comment_users)
		print('writing comments')
		dbutils.write_comments(flat_comments)
		print('comments written')
	return(comment_tree)

@app.get('/write_users')
async def write_users():
	users: list = [{'id': '31',
		'username': 'a',
		'acct': 'a',
		'display_name': 'Andrew Torba ✝️',
		'locked': False,
		'bot': False,
		'created_at': '2016-08-10T06:02:25.000Z',
		'note': '<p>Saved servant soldier of Jesus Christ the King of Kings. Husband, Father, and the CEO of <a data-focusable="true" role="link" href="https://gab.com/gab" class="mention">@gab</a>. </p><p>Now faith is the substance of things hoped for, the evidence of things not seen. Hebrews 11:1</p>',
		'url': 'https://gab.com/a',
		'avatar': 'https://media.gab.com/system/accounts/avatars/000/000/031/original/86e4974436280f01.png',
		'avatar_static': 'https://media.gab.com/system/accounts/avatars/000/000/031/original/86e4974436280f01.png',
		'avatar_small': 'https://media.gab.com/cdn-cgi/image/width=92,fit=scale-down/system/accounts/avatars/000/000/031/original/86e4974436280f01.png',
		'avatar_static_small': 'https://media.gab.com/cdn-cgi/image/width=92,fit=scale-down/system/accounts/avatars/000/000/031/original/86e4974436280f01.png',
		'header': 'https://media.gab.com/system/accounts/headers/000/000/031/original/D2DFEEB6-ECA8-44A4-BE57-419AC9BEBD6C.jpeg',
		'header_static': 'https://media.gab.com/system/accounts/headers/000/000/031/original/D2DFEEB6-ECA8-44A4-BE57-419AC9BEBD6C.jpeg',
		'is_spam': False,
		'followers_count': 50,
		'following_count': 2471,
		'statuses_count': 63946,
		'is_pro': True,
		'is_verified': True,
		'is_donor': True,
		'is_investor': False,
		'show_pro_life': True,
		'emojis': [],
		'fields': [{'name': 'Who Is Andrew Torba?',
		'value': '<a href="http://andrewtorba.com" rel="me nofollow noopener noreferrer" target="_blank"><span aria-hidden="true" class="invisible">http://</span>andrewtorba.com<span aria-hidden="true" class="invisible"></span></a>',
		'verified_at': None},
		{'name': 'Upgrade to GabPRO',
		'value': '<a href="https://pro.gab.com" rel="me nofollow noopener noreferrer" target="_blank"><span aria-hidden="true" class="invisible">https://</span>pro.gab.com<span aria-hidden="true" class="invisible"></span></a>',
		'verified_at': None},
		{'name': 'Shop Gab Merch',
		'value': '<a href="https://shop.gab.com" rel="me nofollow noopener noreferrer" target="_blank"><span aria-hidden="true" class="invisible">https://</span>shop.gab.com<span aria-hidden="true" class="invisible"></span></a>',
		'verified_at': None},
		{'name': 'Read Gab News',
		'value': '<a href="https://news.gab.com" rel="me nofollow noopener noreferrer" target="_blank"><span aria-hidden="true" class="invisible">https://</span>news.gab.com<span aria-hidden="true" class="invisible"></span></a>',
		'verified_at': None},
		{'name': 'Watch Gab TV',
		'value': '<a href="https://tv.gab.com" rel="me nofollow noopener noreferrer" target="_blank"><span aria-hidden="true" class="invisible">https://</span>tv.gab.com<span aria-hidden="true" class="invisible"></span></a>',
		'verified_at': None}]},
		{'id': '5020786',
		'username': 'KathyBarnetteForSenate',
		'acct': 'KathyBarnetteForSenate',
		'display_name': 'Kathy Barnette',
		'locked': False,
		'bot': False,
		'created_at': '2021-04-12T00:31:43.603Z',
		'note': '<p>Candidate for US Senate from Pennsylvania.<br />Pennsylvania First. America First.</p><p><a href="https://BarnetteForSenate.com" rel="nofollow noopener noreferrer" target="_blank"><span aria-hidden="true" class="invisible">https://</span>BarnetteForSenate.com<span aria-hidden="true" class="invisible"></span></a><br /><a href="https://secure.winred.com/kathybarnette/senate-donate" rel="nofollow noopener noreferrer" target="_blank"><span aria-hidden="true" class="invisible">https://</span>secure.winred.com/kathybarnette/senate-donate<span aria-hidden="true" class="invisible"></span></a></p>',
		'url': 'https://gab.com/KathyBarnetteForSenate',
		'avatar': 'https://media.gab.com/system/accounts/avatars/005/020/786/original/4de3e2f990414068.jpg',
		'avatar_static': 'https://media.gab.com/system/accounts/avatars/005/020/786/original/4de3e2f990414068.jpg',
		'avatar_small': 'https://media.gab.com/cdn-cgi/image/width=92,fit=scale-down/system/accounts/avatars/005/020/786/original/4de3e2f990414068.jpg',
		'avatar_static_small': 'https://media.gab.com/cdn-cgi/image/width=92,fit=scale-down/system/accounts/avatars/005/020/786/original/4de3e2f990414068.jpg',
		'header': 'https://media.gab.com/system/accounts/headers/005/020/786/original/d06387e471af859d.jpg',
		'header_static': 'https://media.gab.com/system/accounts/headers/005/020/786/original/d06387e471af859d.jpg',
		'is_spam': False,
		'followers_count': 38972,
		'following_count': 28,
		'statuses_count': 454,
		'is_pro': True,
		'is_verified': True,
		'is_donor': False,
		'is_investor': False,
		'show_pro_life': False,
		'emojis': [],
		'fields': []}]
	dbutils.write_users(users)

@app.get('/fetch_posts')
async def fetch_posts():
	posts: list = su.get_posts(1)
	return posts

@app.get('/test_add')
async def __add_test_post__():
	output = dbutils.__add_test_post__()

@app.get('/test_get')
async def __get_first_post__():
	output = dbutils.__get_first_post__()
	return output