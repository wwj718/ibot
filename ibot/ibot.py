# -*- coding: utf-8 -*-
# six
from distutils.log import warn as printf
import sys
from bosonnlp import BosonNLP
import yaml
from os.path import expanduser
import os
import collections
import subprocess
import datetime

home = expanduser("~")
with open(os.path.join(home,".ibot.yml")) as f:
    config = yaml.load(f)
    bosonnlp_token = config["token"]

#bosonnlp/client.py
#LOGGING_FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
# 使logging.basicConfig(format=LOGGING_FORMAT, level=logging.ERROR)，不出现标志


class QueryParser(object):
    def __init__(self):
        self.nlp = BosonNLP(bosonnlp_token)
    def parse(self, query_string):
        """
        input:
        7月22号 北京到上海的高铁票
        output:
        [{'entity': [[0, 3, 'time'], [3, 4, 'location'], [5, 6, 'location']], # 需要理解实体出现的模式，这块需要理解上下文
        'tag': ['t', 'm', 'q', 'ns', 'p', 'ns', 'ude', 'n', 'n'],
         'word': ['7月', '22', '号', '北京', '到', '上海', '的', '高铁', '票']}]
        """
        result = self.nlp.ner(query_string)[0]
        words = result['word']
        tags = result['tag']
        entities = result['entity']
        return (words,entities,tags)
    def get_entity(self,parsed_words,index_tuple):
        """
        获取已识别的实体
        采用filter
        参考 python cookbook部分

        input:
            entities : 二元组
            parsed_words : 解析好的词组
        """
        return parsed_words[index_tuple[0]:index_tuple[1]]

    def format_entities(self,entities):
        """
        给元组命名
        """
        namedentity = collections.namedtuple('namedentity','index_begin index_end entity_name')
        return [namedentity(entity[0],entity[1],entity[2]) for entity in entities]

    def get_format_time(self,time_entity):
        """
        output
        {'timestamp': '2013-02-28 16:30:29', 'type': 'timestamp'}
        """
        basetime = datetime.datetime.today()
        result = self.nlp.convert_time(
            time_entity,
            basetime)
        #print(result)
        timestamp = result["timestamp"]
        return timestamp.split(" ")[0]



def call_iquery_train_ticket(location_from_entity,location_to_entity,time_entity):
    printf(subprocess.call(["iquery",location_from_entity,location_to_entity,time_entity]))

def pattern_train_ticket(query):
    query_parse = QueryParser()
    (words,entities,tags) = query_parse.parse(query)
    #给元组命名，整体filter
    namedentities = query_parse.format_entities(entities) # 检查实体的数量，count ，元组，token
    # 写个if语句，然后才进入这里
    time_nameentity = [nameentity for nameentity in namedentities if nameentity.entity_name=="time"][0] # 假设只有一个
    location_nameentities = [nameentity for nameentity in namedentities if nameentity.entity_name=="location"] # 假设有2个
    sorted_location_nameentities = sorted(location_nameentities,key=lambda a:a[1])
    # 排序为有序列表 list.sort() 按照第一个元素排序 sorted(a),按顺序,sorted(a,key=lambda a:a[1]) 按第二个元素排序
    time_entity =  query_parse.get_entity(words,(time_nameentity.index_begin,time_nameentity.index_end))
    time_string = "".join(time_entity)
    format_time = query_parse.get_format_time(time_string)

    location_from_nameentity = sorted_location_nameentities[0] #较前边的,出发地
    location_from_entity =  query_parse.get_entity(words,(location_from_nameentity.index_begin,location_from_nameentity.index_end))
    location_from_string = "".join(location_from_entity)

    location_to_nameentity = sorted_location_nameentities[1] #较后边的，目的地:w
    location_to_entity =  query_parse.get_entity(words,(location_to_nameentity.index_begin,location_to_nameentity.index_end))
    location_to_string = "".join(location_to_entity)

    #printf(u"捕获时间:{}".format(time_string))
    #printf(u"出发地:{}".format(location_from_string))
    #printf(u"目的地:{}".format(location_to_string))

    # 正式查询
    call_iquery_train_ticket(location_from_string,location_to_string,format_time)
    return




def main():
    query = " ".join(sys.argv[1:])
    printf(query)
    printf("*"*8)
    pattern_train_ticket(query)

if __name__ == '__main__':
    main()
