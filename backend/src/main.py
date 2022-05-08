from fastapi import FastAPI
import utils.scraper_utils as su
import utils.database_utils as dbutils

app = FastAPI()

@app.get('/test_get')
async def get_first_post():
	output = dbutils.get_first_post()
	return output

@app.get('/fetch_posts')
async def fetch_posts():
	info = su.get_posts(1)
	return info