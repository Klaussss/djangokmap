from django.shortcuts import render
from django.http import HttpResponse
import os;
import json
import re
from pymongo import MongoClient

# Create your views here.
def display(request):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.mydb
    relation_set = db.paper_relation_set

    if request.method == "POST":
        source = request.POST.get("key");
        print('source')
    else:
        klist =list(relation_set.find({},{"_id":0}).limit(1))
        source = klist[0]["source"]
    return givepage(request,source);

def givepage(request,source):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.mydb
    relation_set = db.paper_relation_set
    property_set = db.paper_property_set

    print ("------Search Key:"+source)
    # Get the relation set
    klist =list(relation_set.find({"source":re.compile(source)},{"_id":0}))
    klist +=list(relation_set.find({"target":re.compile(source)},{"_id":0}))

    print ("------Size of the search result: "+ str(len(klist)))

    # Get the property set
    list_item = list(set([i["source"] for i in klist ]+[i["target"] for i in klist]))
    list_itemdic = [];
    for item in list_item:
        list_itemdic += list(property_set.find({"Title":item},{"_id":0})) 

    return render(request,"display/map.html",{'Dict':json.dumps(klist),'List':list_itemdic}) 

def displaybykey(request,key):
    return givepage(request,key);
