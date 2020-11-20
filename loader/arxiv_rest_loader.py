import urllib.request as libreq
import re

import feedparser


class ArxivRestLoader:
    title_parse_cleaner = re.compile('\(.+\[.+\].*\)')
    html_tag_cleaner = re.compile('<.*?>')

    def __init__(self, categories, sort_order, max_results):
        self.categories = categories
        self.sort_order = sort_order
        self.max_results = max_results
        self.base_url = 'http://export.arxiv.org/api/query?search_query='

    def generate_url(self):
        str_list = []
        str_list.append(self.base_url)
        for idx, category in enumerate(self.categories):
            # http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:q-bio.BM&max_results=20
            if idx == 0:
                str_list.append('cat:')
                str_list.append(category)
            else:
                str_list.append('+')
                str_list.append('OR')
                str_list.append('+')
                str_list.append('cat:')
                str_list.append(category)
        if self.max_results:
            str_list.append('&')
            str_list.append('max_results=')
            str_list.append(str(self.max_results))
        if self.sort_order:
            str_list.append('&')
            str_list.append('sortBy=')
            str_list.append(self.sort_order)
        return ''.join(str_list)

    def get_papers(self):
        results = []
        url = self.generate_url()
        with libreq.urlopen(url) as url:
            results.append(url.read())

        papers = []
        for result in results:
            parsed_response = feedparser.parse(result)
            for entry in parsed_response['entries']:
                title = entry['title'].replace('\n', ' ').replace('\r', ' ')
                abstract = entry['summary'].replace('\n', ' ').replace('\r', ' ')
                paper_obj = {
                    'id': entry['id'],
                    'title': re.sub(self.title_parse_cleaner, '', title),
                    'abstract': re.sub(self.html_tag_cleaner, '', abstract),
                    'link': entry['link'],
                }
                papers.append(paper_obj)
        return papers


if __name__ == "__main__":
    ar = ArxivRestLoader(['cs.AI', 'cs.CC', 'cs.CE'], 'submittedDate', 100)
    results = ar.get_papers()
    # into cassandra u will go!
    print(results)
