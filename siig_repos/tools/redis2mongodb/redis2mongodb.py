####################################
# Read data from redis
# Format it and save into mongoDB
####################################

import sys

class formatredis:
    dictstr = dict();

    def __init__(self,indictstr):
        self.dictstr = indictstr;

    def sourcefunc(self,indictstr):
        return "";

    def targetfunc(self,indictstr):
        return "";

    def relafunc(self,indictstr): 
        return "undefined";

    def typefunc (self,indictstr): 
        return "resolved";

    def formatstring(self):
        outdict = dict();
        outdict["source"]           = self.sourcefunc (self.dictstr);
        outdict["target"]           = self.targetfunc(self.dictstr);
        outdict["rela"]             = self.relafunc(self.dictstr);
        outdict["type"]             = self.typefunc(self.dictstr);
        return outdict

class formatstring(formatredis):
    def targetfunc(self,dicstr):
        try:
            strout = "lat:"+dicstr["location,lat"].split(".")[0] + ",lng:" + dicstr["location,lng"].split(".")[0]
            return strout
        except Exception as err:
            return "";

    def sourcefunc(self,dicstr):
        try:
            namelist =  dicstr["key"].split(":") 
            return namelist[len(namelist)-1]
        except Exception as err:
            return ""

sys.path.append("/home/cuichao/GitRepos/JZXN-C-DATA")
from RedisLib import redis_cli 
# Build an connection to redis
connectpar = {
        "host":'127.0.0.1',
        "port":6379,
        "db":0
        }
red = redis_cli.hashRedis(connectpar)
pathbase = "SmallCompany:Lifadian:basic:20190117:"

# Connect to mongoDB:
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
relation_set = db.relation_set
property_set = db.property_set

allkeys = red.r.keys(pathbase+"*")

for key in allkeys:
    dictstr = red.hgetall(key)

    print(dictstr)

    dictstr["key"] = key.decode()
    
    formatstr = formatstring(dictstr) 
    dictstr["id__"] = formatstr.sourcefunc(dictstr) 
    property_set.insert(dictstr)
    result = formatstr.formatstring()
    relation_set.insert(result)
