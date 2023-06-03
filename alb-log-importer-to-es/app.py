import os
import json
import time
import pandas as pd
import itertools
from elasticsearch import Elasticsearch, helpers

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ES_HOST = os.getenv("hostName", 'localhost')
TARGET_FILE = os.getenv(
    "targetFile", 'alb.tsv')


def lambda_handler(event, context):
    def chunked_iterable(iterable, chunk_size):
        it = iter(iterable)
        while True:
            chunk = tuple(itertools.islice(it, chunk_size))
            if not chunk:
                return
            yield chunk

    client = Elasticsearch(
        [ES_HOST],
        scheme="http",
        port=9200,
    )

    csv_file = event['target_file'] if 'target_file' in event else TARGET_FILE
    filename = f"./{csv_file}"
    _csv = os.path.basename(filename)
    index_name, _ = os.path.splitext(_csv)

    df = pd.read_csv(filename, sep='\t')
    data_json = df.to_json(orient='records')

    data = json.loads(data_json)

    chunk_size = 1000

    for chunk in chunked_iterable(data, chunk_size):
        actions = [
            {
                "_index": index_name,
                "_source": record,
            }
            for record in chunk
        ]

        helpers.bulk(client, actions)
        time.sleep(1)
        print(f'Indexed {len(actions)} documents')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f'{index_name} created',
        }),
    }


if __name__ == '__main__':
    event = {}
    res = lambda_handler(event=event, context=None)

    print(res)
