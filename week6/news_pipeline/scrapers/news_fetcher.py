import logging
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..','common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://hfuxchlq:ZMeJMeLngGx-A9uDwK1aL0B3mEioq19e@lion.rmq.cloudamqp.com/hfuxchlq"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap_news_scrape_news_task_queue"
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://fbwfsbki:Ec6Am2ZaSrnZ0qqgAHrinRXJIueHI4jr@chimpanzee.rmq.cloudamqp.com/fbwfsbki"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap_news_scrape_news_task_queue"

SLEEP_TIME_IN_SECONDS = 5

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('news_fetcher')
logger.setLevel(logging.DEBUG)

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL,DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL,SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
	if msg is None or not isinstance(msg,dict):
		logger.warning('message is broken')
		return

	text=None

	if(msg['source']=='cnn'):
		text=cnn_news_scraper.extract_news(msg['url'])

	msg['text']=text
	#to do:re_connect is lost
	dedupe_news_queue_client.sendMessage(msg)

def run():
	while True:
		if scrape_news_queue_client is not None:
			msg=scrape_news_queue_client.getMessage()
			if msg is not None:
				try:
					handle_message(msg)
				except Exception as e:
					logger.warning(e)
					pass
			scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ =='__main__':
	run()
