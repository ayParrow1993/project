import logging
import json
import os
import sys
import operations
from bson.json_util import dumps
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

sys.path.append(os.path.join(os.path.dirname(__file__),'utils'))
import mongodb_client # pylint: disable=import-error, wrong-import-position

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format = logger_format)
logger = logging.getLogger('backend_server')
logger.setLevel(logging.DEBUG)

def add(num1,num2):
	"""  test method. """
	logger.debug("add is called with %d anf %d", num1 ,num2)
	return operations.add(num1,num2)

def get_one_news():
	""" test method to get one news """
	logger.debug('getonenews is called')
	res = mongodb_client.get_db()['news'].find_one()
	return operations.get_one_news()

def get_news_summaries_for_user(user_id,page_num):
	logger.debug('get_news_summaries_for_user is called with %s and %s',user_id,str(page_num))
	return operations.get_news_summaries_for_user(user_id,page_num)

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(add,'add')
RPC_SERVER.register_function(get_one_news,'getOneNews')
RPC_SERVER.register_function(get_news_summaries_for_user,'getNewsSummariesForUser')




logger.info("starting rpc server on %s:%d", SERVER_HOST, SERVER_PORT)
RPC_SERVER.serve_forever()