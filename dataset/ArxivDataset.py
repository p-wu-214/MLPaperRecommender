from config import config
from elasticsearch import Elasticsearch
from torch.utils.data import Dataset

es_config = config.elasticsearch_config


def get_data():
    es = Elasticsearch()
    res = es.search(index=es_config['index'], body={"size": 10000, "query": {"match_all": {}}})
    print(res)
    result = {
        'length': res['hits']['total'],
        'data': res['hits']['hits']
    }
    return result


if __name__ == "__main__":
    get_data()


class ArxivDataset(Dataset):
    def __init__(self):
        res = get_data()
        self.data = res['data']
        self.length = res['length']

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return self.length
