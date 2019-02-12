from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from viewfolder.models import Folder
import os

# Create your views here.
def personalfolder(request,username):
    if request.session.get(username,"none")==username:
        html = "viewfolder/personalfolder.html";
        return folder_operation(request,username,username,html);
    else:
        return HttpResponse("Please login first");

class Upload(forms.Form):
    filepath = forms.FileField();
    description = forms.CharField();

def publicfolder(request,username):
    if request.session.get(username,"none")==username:
        html = "viewfolder/publicfolder.html";
        return folder_operation(request,"public",username,html);
    else:
        return HttpResponse("Please login first");

def readfile(path,buf_size=262144):
    with open(path,"rb") as fd:
        while True:
            c = fd.read(buf_size);
            if c:
                yield c;
            else:
                break;

def getfile(request,username, filename):
    path = "./folder/"+username+"/"+filename
    response = HttpResponse(readfile(path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(path);
    return response;

def deletefile(request,username,filename):
    path = "./folder/"+username+"/"+filename
    Folder.objects.filter(username=username,filepath=filename).delete();
    os.remove(path);
    return HttpResponse("File "+filename+" is deleted successfully");

def folder_operation(request,username,uploadname,html):
    if request.method=="POST":

        filename = request.POST.get("description");
        filepath = request.FILES["filepath"];

        if Folder.objects.filter(username=username,filepath=filepath).count():
            return HttpResponse("File "+filepath.name+" already exits");

        upload = Folder();
        upload.filename = filename;
        upload.filepath = filepath.name;
        upload.username = username;

        upload.save();

        SavePath = "./folder/"+username+"/"+filepath.name;
        with open(SavePath,"wb") as fw:
            for chunk in filepath.chunks():
                fw.write(chunk);

        return HttpResponse("Upload successfully!");
        
    else:
        upload = Upload();
        files = Folder.objects.filter(username=username);
        path = "/folder/"+username+"/"
        # form files as a filder
        File = [];
        for i in range(len(files)):
            filetmp = [];
            filetmp.append(str(files[i].username));
            filetmp.append(str(files[i].filepath));
            filetmp.append(str(files[i].filename));
            File.append(filetmp);
        return render(request,html,{"username":uploadname,'upload':upload,"files":File,"path":path})
