# Alb log importer to Elasticsearch

## required
* docker
* python

## tools setup

```bash
% cd alb-log-importer-to-es                              
% pwd
/path/to/directory/tools/alb-log-importer-to-es
$ pip3 install -r requirements.txt
```

## elasticsearch start

```bash
docker-compose up -d
```

## log import

```bash
targetFile=alb.tsv python3 app.py
```

* log

```
% targetFile=alb.tsv python3 app.py
Indexed 1000 documents
Indexed 1000 documents
Indexed 196 documents
{'statusCode': 200, 'body': '{"message": "alb created"}'}
```

## kibana url

http://localhost:5601/app/dev_tools#/console

## query by kibana

```kibana
GET alb/_search
{
  "query": {
    "range": {
      "target_processing_time": {
        "gte": 10
      }
    }
  },
  "sort": [
    {
      "target_processing_time": {
        "order": "desc"
      }
    }
  ]
}
```