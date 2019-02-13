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
    my_set = db.test_set

    if request.method == "POST":
        source = request.POST.get("key");
    else:
        klist =list(my_set.find({},{"_id":0}).limit(1))
        source = klist[0]["source"]
    return givepage(request,source);

def givepage(request,source):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.mydb
    my_set = db.test_set

    klist =list(my_set.find({"source":re.compile(source)},{"_id":0}).limit(30))
    klist +=list(my_set.find({"target":re.compile(source)},{"_id":0}).limit(30))
    return render(request,"display/map.html",{'Dict':json.dumps(klist),'List':klist}) 

def displaybykey(request,key):
    return givepage(request,key);
