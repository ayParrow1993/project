import operations

def test_getNewsSummariesForUser_basic():
	news = operations.get_news_summaries_for_user('test',1)
	assert len(news)>0
	print(len(news))
	print('test_getNewsSummariesForUser_basic passed!')

def test_getNewsSummariesForUser_pagination():
	news1 = operations.get_news_summaries_for_user('parrow',1)
	news2 = operations.get_news_summaries_for_user('parrow',2)
	assert len(news1)>0
	print(len(news1))
	assert len(news2)>0
	print(len(news2))
	digests_page_1_set = set([news['digest'] for news in news1])
	digests_page_2_set = set([news['digest'] for news in news2])
	assert len(digests_page_1_set.intersection(digests_page_2_set))==0
	print('digest passed!')

if __name__ == "__main__":
	test_getNewsSummariesForUser_basic()
	test_getNewsSummariesForUser_pagination()
