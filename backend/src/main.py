from fastapi import FastAPI
import utils.scraper_utils as su
import utils.database_utils as dbutils

app = FastAPI()

@app.get('/fetch_posts')
async def fetch_posts():
	info = su.get_posts(1)
	return info

@app.get('/test_add')
async def __add_test_post__():
	output = dbutils.__add_test_post__()

@app.get('/test_get')
async def __get_first_post__():
	output = dbutils.__get_first_post__()
	return output