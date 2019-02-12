from django.shortcuts import render
from django.http import HttpResponse
import os;
import json
from pymongo import MongoClient

# Create your views here.
def display(request):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.mydb
    my_set = db.test_set

    klist =list(my_set.find({},{"_id":0}).limit(50))
    return render(request,"display/map.html",{'Dict':json.dumps(klist)}) 
