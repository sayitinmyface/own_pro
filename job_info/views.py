from django.shortcuts import render
from pymongo import MongoClient

# Create your views here.
def jobinfolist(req):
    db_url = 'mongodb://192.168.219.116:27017'
    with MongoClient(db_url) as client:
        mydb = client['mydb']
        collection = mydb['startupinfo']
        result = list(collection.find())
    return render(req,'job_info/jobinfolist.html',{'info':result})
# 
def jobinfodetail(req,title):
    db_url = 'mongodb://192.168.219.116:27017'
    with MongoClient(db_url) as client:
        mydb = client['mydb']
        collection = mydb['startupinfo']
        result = list(collection.find({'post_title':title}))
    return render(req,'job_info/jobinfodetail.html',{'info':result[0]})