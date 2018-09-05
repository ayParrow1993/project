import json
import os
import pickle
import redis
import sys

from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__),'..','common'))

import mongodb_client

REDIS_HOST='localhost'
REDIS_PORT=6379
USER_NEWS_TIME_UP_IN_SECONDS = 3600

NEWS_TABLE_NAME = "news_test"


NEWS_LIMIT = 100
NEWS_LIST_BATCH_SIZE = 10

redis_client = redis.StrictRedis(REDIS_HOST,REDIS_PORT)

def add(num1,num2):
	"""  test method. """
	
	return num1+num2

def get_one_news():
	""" test method to get one news """
	logger.debug('getonenews is called')
	res = mongodb_client.get_db()['news'].find_one()
	return json.loads(dumps(res))

def get_news_summaries_for_user(user_id,page_num):
	page_num = int(page_num)
	begin_index=(page_num-1)*NEWS_LIST_BATCH_SIZE
	end_index=page_num*NEWS_LIST_BATCH_SIZE

	sliced_news = []
	db = mongodb_client.get_db()

	if redis_client.get(user_id) is not None:
		news_digests = pickle.loads(redis_client.get(user_id))
		sliced_news_digests = news_digests[begin_index:end_index]
		
		sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
	else:
		total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt',-1)]).limit(NEWS_LIMIT))
		total_news_digests = [x['digest'] for x in total_news]

		redis_client.set(user_id,pickle.dumps(total_news_digests))
		redis_client.expire(user_id,USER_NEWS_TIME_UP_IN_SECONDS)

		sliced_news = total_news[begin_index:end_index]

	for news in sliced_news:
		del news['text']

	return json.loads(dumps(sliced_news))

