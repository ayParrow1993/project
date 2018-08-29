from cloudAMQP_client import CloudAMQPClient

TEST_CLOUDAMQP_URL = "amqp://hfuxchlq:ZMeJMeLngGx-A9uDwK1aL0B3mEioq19e@lion.rmq.cloudamqp.com/hfuxchlq"
TEST_QUEUE_NAME = "test"

def test_basic():
	client = CloudAMQPClient(TEST_CLOUDAMQP_URL, TEST_QUEUE_NAME)

	sentMsg = {'test':'123'}
	client.sendMessage(sentMsg)
	client.sleep(3)
	receivedMsg = client.getMessage()

	assert sentMsg == receivedMsg
	print('test_basic passed!')

if __name__ == '__main__':
	test_basic()

