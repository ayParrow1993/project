import json
import os
import sys

from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__),'..','common'))

import mongodb_client

SERVER_HOST = 'localhost'
SERVER_PORT = 4040


def add(num1,num2):
	"""  test method. """
	
	return num1+num2

def getOneNews():
	""" test method to get one news """
	logger.debug('getonenews is called')
	res = mongodb_client.get_db()['news'].find_one()
	return json.loads(dumps(res))

