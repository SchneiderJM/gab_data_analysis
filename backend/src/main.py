from fastapi import FastAPI
import utils.scraper_utils as su
import logging

logger = logging.getLogger('api')
app = FastAPI()


@app.get('/fetch_posts')
async def fetch_posts():
	info = su.get_posts(1)
	logger.debug(info)
	return info