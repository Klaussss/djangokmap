from django.shortcuts import render
from django.http import HttpResponse
import os;

# Database :
from userlogin.models import AccountInfo;

# Create your views here.
def login(request):
   return render(request,"login/login.html") 

def checkinfo(request):
    if request.method == "POST":
        Username = request.POST.get("username");
        Password = request.POST.get("password");

        failed = 0;
        # Check if the input is valid 
        if Username == "" or Password == "":
            reason = "Input is invalid";
            failed = 1;
        # Check if the account is exit
        elif AccountInfo.objects.filter(username=Username).count()==0:
            reason = "Account does not exist"
            failed = 1;
        # Check the username and the password;
        else:
            passwordDB = AccountInfo.objects.filter(username=Username)[0].password;
            reason = "Password and Username are unmatched";
            if not passwordDB == Password:
                failed = 1;

        if failed==1:
            return render(request,"login/loginfail.html",{"reason":reason})
        else:
            request.session[Username] = Username
            return render(request,"login/loginsuccess.html",{"username":Username,"password":Password})
    return HttpResponse("Error!");

def getregisterinfo(request,params):
    params["username"]       = request.POST.get("username")
    params["password"]       = request.POST.get("password")
    params["chinesename"]    = request.POST.get("chinesename")
    params["researchtopic"]  = request.POST.get("researchtopic")
    params["grade"]          = request.POST.get("grade")
    params["hometown"]       = request.POST.get("hometown")
    params["phonenumber"]    = request.POST.get("phonenumber")
    params["email"]          = request.POST.get("email")
    return params;

def register(request):
    if request.method == "POST":
        Username = request.POST.get("username");
        Password = request.POST.get("password");
        params = dict();
        params = getregisterinfo(request,params);

        failed = 0;
        # Check if the input is valid 
        if Username == "" or Password == "":
            reason = "Input is invalid";
            failed = 1;
        # Check if the account is exit
        elif not AccountInfo.objects.filter(username=Username).count()==0:
            reason = "Account already exist, change a new name please"
            failed = 1;
        # Check the username and the password;
        else:
            p = AccountInfo.objects.create(**params);
            p.save();
            # Make a personal folder for current user
            os.makedirs("./folder/"+Username)
            return render(request,"login/login.html")

        if failed==1:
            return render(request,"login/loginfail.html",{"reason":reason})

    else:
        return render(request,"login/register.html")
def logout(request,username):
    del request.session[username];
    return HttpResponse("LogoutSuccessfully!")
