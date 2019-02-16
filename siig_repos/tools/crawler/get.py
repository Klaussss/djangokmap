import sys,getopt
from urllib import parse
sys.path.append("/home/cuichao/GitRepos/JZXN-C-DATA/Crawler")
sys.path.append("/home/cuichao/GitRepos/JZXN-C-DATA")

from RedisLib import redis_cli 
from package import baiduapi 
from package import getInfoWeb 
from urllib.parse import urlsplit

import json

opts,args = getopt.getopt(sys.argv[1:],"k:")
prompt= '''
        Usage:
        python get.py -k "key" 
        '''

for k,v in opts:
    if k == "-k":
        key = v;
    else:
        print(prompt) 

# Connect to the redis 
connectpar = {
        "host":'127.0.0.1',
        "port":6379,
        "db":0
        }

red = redis_cli.hashRedis(connectpar)

# Add something new to the redis key library
path = "PaperInfoFromBadiXS:"
explain = "Paper information crawled from baidu xueshu ..."
red.IndexKeyput(path,explain)

# Connect to mongoDB:
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
relation_set = db.paper_relation_set
property_set = db.paper_property_set

baseurl = "http://xueshu.baidu.com/s?wd={0}&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D"
            

pattern = {
        "Title":{
            'p':'div[class="main-info"],h3,a',
            'a':'text'
            },
        "Author":{
            'p':'p[class="author_text"],a',
            'a':'text'
            },
        "Abstract":{
            'p':'p[class="abstract"]',
            'a':'text'
            },
        "KeyWords":{
            'p':'p[class="kw_main"],span',
            'a':'text'
            },
        "DOI":{
            'p':'div[class="doi_wr"],p[class="kw_main"]',
            'a':'text'
            },
        "Source":{
            'p':'div[class="allversion_content"],a',
            'a':'text,href'
            }

        }


# First of all, get the serial number of this paper
url = baseurl.format(parse.quote(key))
print ("Url is "+url)
getHandler = getInfoWeb.getInfoWeb(u=url)
code = getHandler.getHtml()
if not code:
    print ("---"+str(code))
    exit(0)

getHandler.setPattern(p='div[id="dtl_main"]',a='data-click')
getHandler.getNode()
result = getHandler.getData()
if result: 
    keygrp = result[0].split('data-click:')[1]
    datajson = json.loads(keygrp.replace("'",'"'))
else:
    print ("--Error while analysis-")
    exit(0)
serialno = datajson["longsign"]

# Get the basic information of current paper ... 
urlbase2='http://xueshu.baidu.com/usercenter/paper/show?paperid={0}'
url = urlbase2.format(parse.quote(serialno))
getHandler = getInfoWeb.getInfoWeb(u=url)
if not getHandler.getHtml():
    print ("---")
    exit(0)

outresult = dict()
for keyget in pattern.keys():
    getHandler.setPattern(p=pattern[keyget]['p'],a=pattern[keyget]['a']);
    getHandler.getNode()
    rawresult =  getHandler.getData()
    outresult[keyget] = []
    for rr in rawresult:
        try:
            outresult[keyget].append(rr.split(pattern[keyget]['a']+":")[1])
        except Exception as err:
            pass
outresult['Source'] = [getHandler.responsehandler.geturl()]

if not outresult['Title']:
    print ("---")
    exit(0)

for i in range(1,len(outresult['DOI'])):
    outresult['DOI'][i] = outresult['DOI'][i].replace('\u0001','')

property_set.insert(outresult)

referenceto="http://xueshu.baidu.com/usercenter/paper/search?wd=citepaperuri%3A({0})&type=reference&rn=10&page_no="
citiedby="http://xueshu.baidu.com/usercenter/paper/search?wd=refpaperuri%3A({0})&type=citation&rn=10&page_no="
relatedto="http://xueshu.baidu.com/usercenter/paper/search?&wd={0}&type=related&rn=10&page_no="

rcr = dict()
rcr["reference"]  =[]
rcr["citied_by"] =[]
rcr["related_to"]=[]

for i in range (1,5): 
    getHandler = getInfoWeb.getInfoWeb(u=referenceto.format(parse.quote(serialno))+str(i))
    jraw = getHandler.getHtml()
    if jraw:
        rcr["reference"]  += [jraw]
    getHandler = getInfoWeb.getInfoWeb(u=citiedby.format(parse.quote(serialno))+str(i))
    jraw = getHandler.getHtml()
    if jraw:
        rcr["citied_by"]  += [jraw]
    getHandler = getInfoWeb.getInfoWeb(u=relatedto.format(parse.quote(key))+str(i))
    jraw = getHandler.getHtml()
    if jraw:
        rcr["related_to"] += [jraw]


outkeys = { 
        "Title":'sc_title',
        "Author0":'sc_author',
        "Abstract":'sc_abstract',
        "KeyWords":'sc_keyword',
        "DOI":'sc_doi',
        "Source":"url"
            }

for keyr in rcr.keys():
    for istr in rcr[keyr]:
        try:
            result_output = json.loads(istr)
            jsondata = result_output['data']['papers']
            for item in jsondata:
                outresult = dict()
                for i in outkeys.keys():
                    try:
                        outresult[i] = (item['meta_di_info'][outkeys[i]])
                    except Exception as err:
                        outresult[i] = ""
                outresult['Author'] = []
                for i in outresult['Author0']:
                    outresult['Author'].append(i['sc_name'][0])
                outresult.pop('Author0')
                if outresult['KeyWords']:
                    outresult['KeyWords'] = outresult['KeyWords'][0].split(",")
                else:
                    outresult['KeyWords'] = []
                outresult['Source'] = [outresult['Source']]

                for i in range(0,len(outresult['DOI'])):
                    outresult['DOI'][i] = outresult['DOI'][i].replace('\u0001','')
                    print (outresult['DOI'][i])

                property_set.insert(outresult)

                # form the relation data here:

                relation = dict();
                relation['source'] = outresult['Title'][0]
                relation['target'] = key
                relation['rela'] = keyr
                relation['type'] = 'resolved'

                relation_set.insert(relation)

            
        except Exception as err:
            pass
