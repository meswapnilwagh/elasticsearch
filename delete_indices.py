# Copyright (C) 2011, 2012 9apps B.V.
# 
# echo "@daily /usr/bin/python elasticsearch/delete_indices.py 14" | crontab -

import os, sys, json

import requests
from time import gmtime,strftime,time

# this we'll have to get from userdata
cluster = "elasticsearch.logstash.adgoji.com"

indexes = "http://{0}:9200/_stats?level=shards"
delete_all = "http://{0}:9200/"
delete_one = "http://{0}:9200/{1}"

def delete_shards(days=7):
    try:
        older = "logstash-{0}".format(strftime("%Y.%m.%d",
        gmtime(time() - int(days) * 24 * 60 * 60)))
        for shard in shards:
            if shard <= older:
                print requests.delete(delete_one.format(cluster, shard)).text
    except:
        pass

if __name__ == '__main__':
    stats = json.load(requests.get(indexes.format(cluster)).raw)
    shards = stats['_all']['indices']
    if len(sys.argv) > 1:
        if "all" == sys.argv[1]:
            for shard in shards:
                print requests.delete(delete_all.format(cluster)).text
        else:
            delete_shards(sys.argv[1])
    else:
        # delete all older then 7 days
        delete_shards()