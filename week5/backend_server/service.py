import logging
import json
import os
import sys
from bson.json_util import dumps
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

sys.path.append(os.path.join(os.path.dirname(__file__),'utils'))
import mongodb_client

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format = logger_format)
logger = logging.getLogger('backend_server')
logger.setLevel(logging.DEBUG)

def add(a,b):
	"""  test method. """
	logger.debug("add is called with %d anf %d", a ,b)
	return a+b

def getOneNews():
	""" test method to get one news """
	logger.debug('getonenews is called')
	res = mongodb_client.get_db()['news'].find_one()
	return json.loads(dumps(res))

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(add,'add')
RPC_SERVER.register_function(getOneNews,'getOneNews')


logger.info("starting rpc server on %s:%d", SERVER_HOST, SERVER_PORT)
RPC_SERVER.serve_forever()