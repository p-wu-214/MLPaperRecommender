from config import config

from datetime import date
import feedparser
import re

from elasticsearch import Elasticsearch

arxiv_config = config.arxiv_config

ELASTICSEARCH_INDEX = 'ml_library'
es = Elasticsearch()

title_parse_cleaner = re.compile('\(.+\[.+\].*\)')
html_tag_cleaner = re.compile('<.*?>')


def get_arxiv_data():
    arxiv_papers_by_category = {}
    for arxiv_category_name, arxiv_category_url in arxiv_config.items():
        papers = []
        category_data = feedparser.parse(arxiv_category_url)
        for entry in category_data['entries']:
            title = entry['title'].replace('\n', ' ').replace('\r', ' ')
            abstract = entry['summary'].replace('\n', ' ').replace('\r', ' ')
            paper_obj = {
                'id': entry['id'],
                'title': re.sub(title_parse_cleaner, '', title),
                'abstract': re.sub(html_tag_cleaner, '', abstract),
                'link': entry['link'],
            }
            papers.append(paper_obj)
        arxiv_papers_by_category[arxiv_category_name] = papers
    return arxiv_papers_by_category


def upload_data_to_es(arxiv_papers_by_category):
    count = 0
    for arxiv_category_name, arxiv_papers in arxiv_papers_by_category.items():
        for paper in arxiv_papers:
            doc = {
                'type': arxiv_category_name,
                'title': paper['title'],
                'abstract': paper['abstract'],
                'link': paper['link'],
                'date_retrieved': date.today()
            }
            es.index(index=ELASTICSEARCH_INDEX, id=paper['id'], body=doc)
            count += 1
    print("uploaded {} papers into es".format(count))


if __name__ == "__main__":
    arxiv_papers_by_category = get_arxiv_data()
    upload_data_to_es(arxiv_papers_by_category)
