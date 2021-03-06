import os
import re
import time
from python_code.model import lda
from python_code.model.ptt_article_fetcher import fetch_articles
from python_code.model.my_tokenize.tokenizer import cut


def log(file, obj):
    print(obj)
    print(obj, end="\n", file=file)


def build_lda_by_keywords(keywords, num_article_for_search, num_topics=0):
    if num_topics == 0:
        num_topics = len(keywords)

    dir_name = '../data'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    filename = dir_name + '/' + str("_".join(keywords) + "_" + str(num_article_for_search))

    with open(filename, 'w', encoding="utf-8") as file:
        articles = []
        for keyword in keywords:
            articles_keyword = fetch_articles(keyword, number=num_article_for_search, days=-1)
            articles.extend(articles_keyword)
            log(file, "%s : %d" % (keyword, len(articles_keyword)))

        texts = []
        for article in articles:
            tokens = cut(
                article.title + article.content, using_stopwords=True, simplified_convert=True)
            texts.append(tokens)

        start = time.time()
        model = lda.build_lda_model(texts, num_topics)
        for topic_key, tokens in lda.get_topic(model, num_topics=num_topics, num_words=15).items():
            log(file, tokens)

        end = time.time()
        log(file, "model train time : " + str(end - start))

        print("\n\n\n\n", file=file)
        for article in articles:
            print(article.title, end="\n", file=file)


def test1():
    keywords_candidate = ['隨機', '巴拿馬', '慈濟']
    key_index_set = [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]
    for num_topics in [10, 20, 50, 100]:
        for key_index in key_index_set:
            keywords = []
            for index in key_index:
                keywords.append(keywords_candidate[index])
            build_lda_by_keywords(keywords, num_topics)


def test2():
    keywords = ['王建民', '柯文哲', '和田光司', '義美', '統神']
    build_lda_by_keywords(keywords, 9)


def one_article_test(article_title):
    build_lda_by_keywords([article_title], 1)


def test_from_log(file_name, clustering_number):
    with open('word2vec_log/clustering_log/' + file_name, 'r', encoding='utf8') as file:
        content = file.read()
        pattern = re.compile('clustering ' + str(clustering_number) + '\n([\W\w]*?)\nclustering')
        titles = re.findall(pattern, content)[0].split('\n')
        for title in titles:
            one_article_test(title)

# one_article_test('蘋果將推iPad Air 3？陸媒曝光規格')
