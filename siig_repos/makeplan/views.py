from django.shortcuts import render
from django.http import HttpResponse
# Database :
from userlogin.models import AccountInfo;
from makeplan.models import *;

# Create your views here.
def makeplan(request,username):
    if not request.session.get(username,"none")==username:
        return HttpResponse("Please Login first");

    # Get all of the users
    if request.method == "GET" :
        params = dict()
        params["inputtype"] = "label"
        params["username"] = username
        makedefaultplan(request,username)
        planid = Plans.objects.filter(username=username)[0].planid;
        params = getparamsplan(request,planid,params,username);
        params = getparamscomment(request,planid,params,username)
        return render(request,"plans/myplan.html",params);

    elif (request.method=="POST" and "saveplan" in request.POST):
        params = dict()
        params["username"] = username
        Plan_dict = getplanfromfront(request,username);
        planid = Plan_dict["planid"]
        # Check if the title already exists
        if not checkifexist(request,username,Plan_dict["planid"]) ==0:
            # To the save session
            del Plan_dict["planid"]
            updateaplan(request,username,planid,Plan_dict)
        else:
            plan = Plans.objects.create(**Plan_dict);
            plan.save;

        params["inputtype"] = "label"

        params = getparamsplan(request,planid,params,username);
        params = getparamscomment(request,planid,params,username)

        return render(request,"plans/myplan.html",params);

    elif (request.method=="POST" and "modifyplan" in request.POST):
        params = dict()
        params["username"] = username
        params["inputtype"] = "edit"
        planid = request.session["planid"]
        params = getparamsplan(request,planid,params,username);
        params = getparamscomment(request,planid,params,username)
        return render(request,"plans/myplan.html",params);

    elif (request.method=="POST" and "searchtitle" in request.POST):
        params = dict()
        params["username"] = username
        params["inputtype"] = "label"
        planid = request.POST.get("searchtitleresult")
        request.session["planid"] = planid
        params = getparamsplan(request,planid,params,username);
        params = getparamscomment(request,planid,params,username)
        return render(request,"plans/myplan.html",params);

    elif (request.method=="POST" and "deleteplan" in request.POST):
        params = dict()
        if deleteaplan(request,username,request.session["planid"]) == 0:
            deletecomments(request,username,request.session["planid"])
            params["username"] = username
            params["inputtype"] = "label"
            makedefaultplan(request,username)
            planid = Plans.objects.filter(username=username)[0].planid;
            request.session["planid"] = planid 
            params = getparamsplan(request,planid,params,username);
            params = getparamscomment(request,planid,params,username)
            return render(request,"plans/myplan.html",params);
        else:
            return HttpResponse("Delete failed")

    elif (request.method=="POST" and "addcomment" in request.POST):
        params = dict()
        planid = request.session["planid"]
        Comment_dict = getcommentfromfront(request,username,username,planid);
        comment = Comment.objects.create(**Comment_dict);
        comment.save();
        params["username"] = username
        params["inputtype"] = "edit"
        params = getparamsplan(request,planid,params,username);
        params = getparamscomment(request,planid,params,username)
        return render(request,"plans/myplan.html",params);

    else:
        params["inputtype"] = "label"
        return render(request,"plans/myplan.html",params);

def getparamsplan(request,planid,params,username):
    params=fillinparams(request,planid,params,username);
    params = gettitle(request,username,params)
    params = getuser(request,params);
    return params;


def getuser(request,params):
    # Get all of the usernames
    Users = AccountInfo.objects.all();
    users = []
    for i in range(len(Users)):
        users.append(Users[i].username)
    params["users"] = users;
    return params

def makedefaultplan(request,username):
    if Plans.objects.filter(username=username).count()==0:
        # Make a default plan here
        defaultplan = Plans.objects.create(username=username);
        defaultplan.save();

def fillinparams(request,planid,params,username):
    Plan = searchaplan(request,planid,username)
    params["shareto"] = Plan.shareto;
    params["planid"] = Plan.planid;
    params["submitto"] = Plan.submitto;
    List_plan = fromdicttolist(request,Plan)
    params["list_plan"] = List_plan;
    return params;

def gettitle(request,username,params):
    # Get all of the title under this username
    Title = Plans.objects.filter(username=username)
    title = []
    for i in range(len(Title)):
        title.append(Title[i].planid)
    params["plantitles"] = title;
    return params


def fromdicttolist(request,Plan_dict):
    List_plan=[];
    List_plan.append(["1",Plan_dict.plan1,Plan_dict.summary1]) 
    List_plan.append(["2",Plan_dict.plan2,Plan_dict.summary2]) 
    List_plan.append(["3",Plan_dict.plan3,Plan_dict.summary3]) 
    List_plan.append(["4",Plan_dict.plan4,Plan_dict.summary4]) 
    List_plan.append(["5",Plan_dict.plan5,Plan_dict.summary5]) 
    List_plan.append(["6",Plan_dict.plan6,Plan_dict.summary6]) 
    List_plan.append(["7",Plan_dict.plan7,Plan_dict.summary7]) 
    return(List_plan)


def getplanfromfront(request,username):
    Plan_dict = dict();
    Plan_dict["username"] = username;
    Plan_dict["planid"] = request.POST.get("planid");
    Plan_dict["plan1"] = request.POST.get("plan1")
    Plan_dict["plan2"] = request.POST.get("plan2")
    Plan_dict["plan3"] = request.POST.get("plan3")
    Plan_dict["plan4"] = request.POST.get("plan4")
    Plan_dict["plan5"] = request.POST.get("plan5")
    Plan_dict["plan6"] = request.POST.get("plan6")
    Plan_dict["plan7"] = request.POST.get("plan7")
    Plan_dict["summary1"] = request.POST.get("summary1")
    Plan_dict["summary2"] = request.POST.get("summary2")
    Plan_dict["summary3"] = request.POST.get("summary3")
    Plan_dict["summary4"] = request.POST.get("summary4")
    Plan_dict["summary5"] = request.POST.get("summary5")
    Plan_dict["summary6"] = request.POST.get("summary6")
    Plan_dict["summary7"] = request.POST.get("summary7")
    Plan_dict["shareto"] = request.POST.get("shareto")
    Plan_dict["submitto"] = request.POST.get("submitto")
    return Plan_dict;

def getcommentfromfront(request,username,commenter,planid):
    Comment_list=dict();
    Comment_list["content"] = request.POST.get("newcomment");
    Comment_list["planid"] = planid;
    Comment_list["username"] = username;
    Comment_list["commenter"] = commenter;
    return Comment_list

def checkifexist(request,username,key):
    return Plans.objects.filter(username=username,planid=key).count()

def getparamscomment(request,planid,params,username):
    Comments = Comment.objects.filter(username=username,planid=planid);
    params["list_comment"] = []
    for comment in Comments:
        params["list_comment"].append([comment.commenter,comment.datetime,comment.content]);
    return params;

def searchaplan(request,planid,username):
    if checkifexist(request,username,planid) == 0:
        makedefaultplan(request,username)
    plan = Plans.objects.filter(username=username,planid=planid)[0]
    if plan:
        return plan;
    else:
        return -1;

def deleteaplan(request,username,planid):
    plan = Plans.objects.filter(username=username,planid=planid)
    if plan:
        Plans.objects.filter(username=username,planid=planid).delete();
        return 0;
    else:
        return -1;

def updateaplan(request,username,planid,Plan):
    Plans.objects.filter(planid=planid,username=username).update(**Plan)

def deletecomments(request,username,planid):
    Comment.objects.filter(username=username,planid=planid).delete()

def getsharer(request,username,params):
    params['list_sharer']  = [];
    Sharer = Plans.objects.filter(shareto=username);
    for sharer in Sharer:
        if not sharer.username in params['list_sharer']:
            params['list_sharer'].append(sharer.username)
    Sharer = Plans.objects.filter(submitto=username);
    for sharer in Sharer:
        if not sharer.username in params['list_sharer']:
            params['list_sharer'].append(sharer.username)
    return params;

def getsharertitle(request,username,sharer,params):
    params['plantitles']  = [];
    Sharer = Plans.objects.filter(username=sharer,shareto=username);
    for sharer in Sharer:
        if not sharer.planid in params['plantitles']:
            params['plantitles'].append(sharer.planid)
    Sharer = Plans.objects.filter(username=sharer,submitto=username);
    for sharer in Sharer:
        if not sharer.planid in params['plantitles']:
            params['plantitles'].append(sharer.planid)
    return params;

# View plan
def viewplan(request,username):
    if not request.session.get(username,"none")==username:
        return HttpResponse("Please Login first");


    # Get all of the users
    if request.method == "GET" :
        params = dict()
        # Get all of the user share to the 
        params["inputtype"] = "label"
        params = getsharer(request,username,params)
        params["username"] = username;
        return render(request,"plans/viewplan.html",params);

    elif (request.method=="POST" and "searchshare" in request.POST):
        params = dict()
        sharer = request.POST.get("searchshareresult")
        request.session["sharer"] = sharer 
        # Get all of the titles 
        params = getsharer(request,username,params)
        params["username"] = username;
        params["sharer"] = request.session["sharer"];
        params = getsharertitle(request,username,request.session["sharer"],params);
        return render(request,"plans/viewplan.html",params);
    elif (request.method=="POST" and "searchtitle" in request.POST):
        params = dict()
        params["inputtype"] = "label"
        title = request.POST.get("searchtitleresult")
        request.session["title"] = title 
        # Get all of the titles and sharetitle 
        params = getsharer(request,username,params)
        params = getsharertitle(request,username,request.session["sharer"],params);

        # Get plan details
        Plan = searchaplan(request,request.session["title"],request.session["sharer"])
        List_plan = fromdicttolist(request,Plan)
        # Basic info
        params["inputtype"] = "label"
        params["sharer"] = request.session["sharer"] 
        params["username"] = username;
        params["planid"] = request.session["title"] 
        params["list_plan"] = List_plan;

        # Get Comments
        params = getparamscomment(request,request.session["title"],params,request.session["sharer"])
        return render(request,"plans/viewplan.html",params);

    elif (request.method=="POST" and "addcomment" in request.POST):
        params = dict()
        planid = request.session["title"]
        Comment_dict = getcommentfromfront(request,request.session["sharer"],username,planid);
        comment = Comment.objects.create(**Comment_dict);
        comment.save();

        # Get all of the titles and sharetitle 
        params = getsharer(request,username,params)
        params = getsharertitle(request,username,request.session["sharer"],params);
        # Get plan details
        Plan = searchaplan(request,request.session["title"],request.session["sharer"])
        List_plan = fromdicttolist(request,Plan)
        params["list_plan"] = List_plan;

        # Get Comments
        params = getparamscomment(request,request.session["title"],params,request.session["sharer"])
        # Basic info
        params["inputtype"] = "label"
        params["sharer"] = request.session["sharer"] 
        params["username"] = username;
        params["planid"] = request.session["title"] 
        params["list_plan"] = List_plan;
        return render(request,"plans/viewplan.html",params);

    else:
        params["inputtype"] = "label"
        return render(request,"plans/viewplan.html",params);
