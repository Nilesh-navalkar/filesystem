from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as li,authenticate,logout
from django.contrib.auth.models import User
from .models import folders,files

icon={'docx':'file-word','doc':'file-word','png':'image','jpg':'image','jpeg':'image','txt':'file','json':'brackets-curly','pdf':'file-pdf'}
# Create your views here.
def landing(request):
    return render(request,'landing.html')

@login_required(login_url="login")
def collections(request):
    current_url = request.build_absolute_uri()+'/'
    # l=request.build_absolute_uri().split('/')
    # print(l)
    if request.method=='POST':
        if 'file' in request.FILES:
            file=request.FILES.get('file')
            newfile=files.objects.create(email=request.user.username,foldername='',file=file,filename=file.name)
            newfile.save()
        foldername=request.POST.get('foldername')
        if foldername is not None:
            if folders.objects.filter(foldername=foldername).exists():
                messages.error(request,'You already have a folder with same name')
                return redirect(request.path_info)
            newfolder=folders.objects.create(email=request.user.username,foldername=foldername,parent='')
            newfolder.save()
            # print(foldername)
    foldersref=folders.objects.filter(email=request.user.username,parent='')
    f=[]
    for folder in foldersref:
        f.append(folder.foldername)
        filesref=files.objects.filter(email=request.user.username,foldername='')
    fls=[]
    for file in filesref:
        if file.foldername!='':
            fls.append([file.filename,file.file,file.foldername,icon[file.filename.split('.')[-1]]])
        else:
            fls.append([file.filename,file.file,'root',icon[file.filename.split('.')[-1]]])
    return render(request,'collections.html',{'folders':f,'url':current_url,'files':fls,'icon':''})

@login_required(login_url="login")
def delete(request,fldn,fn):
    if fn!='':
        if fldn=='root':
            fldn=''
        filesref=files.objects.filter(email=request.user.username,foldername=fldn,filename=fn)
        filesref.delete()
        messages.error(request,"file deleted")
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request,'navigation.html')

@login_required(login_url="login")
def navigation(request,url_params):
    current_url = request.build_absolute_uri()
    l=request.build_absolute_uri().split('/')
    # print(l)
    parent=l[-2]
    if request.method=='POST':
        if 'file' in request.FILES:
            file=request.FILES.get('file')
            newfile=files.objects.create(email=request.user.username,foldername=parent,file=file,filename=file.name)
            newfile.save()
        foldername=request.POST.get('foldername')
        if foldername is not None:
            if folders.objects.filter(foldername=foldername).exists():
                messages.error(request,'You already have a folder with same name')
                return redirect(request.path_info)
            newfolder=folders.objects.create(email=request.user.username,foldername=foldername,parent=parent)
            newfolder.save()
    foldersref=folders.objects.filter(email=request.user.username,parent=parent)
    filesref=files.objects.filter(email=request.user.username,foldername=parent)
    f=[]
    fls=[]
    for folder in foldersref:
        f.append(folder.foldername)
    for file in filesref:
        if file.foldername!='':
            fls.append([file.filename,file.file,file.foldername,icon[file.filename.split('.')[-1]]])
            # print(fls[0][3])
        else:
            fls.append([file.filename,file.file,'root',icon[file.filename.split('.')[-1]]])
    return render(request,'navigation.html',{'folders':f,'url':current_url[21:],'files':fls})

def signup(request):
    if request.method=="POST":
        un=request.POST.get("email")
        pass1=request.POST.get("pass1")
        pass2=request.POST.get("pass2")
        if pass1!=pass2:
            messages.error(request,"passwords dont match")
            return redirect("signup")
        elif User.objects.filter(username=un).exists():
            messages.error(request,"username already exits")
            return redirect("signup")
        else:
            u=User.objects.create_user(username=un,email=un,password=pass1)
            u.save()
            messages.error(request,"account created")
            return redirect("login")
    return render(request,"signup.html")

def login(request):
    if request.method=="POST":
        un=request.POST.get("email")
        p=request.POST.get("pass")
        user=authenticate(username=un,password=p)
        if user is not None:
            li(request,user)
            return redirect("collections")
        else:
            messages.error(request,"invalid credentials")
            return redirect("log_in")
            
    return render(request,"login.html")

@login_required(login_url="login")
def log_out(request):
    logout(request) 
    return redirect("login")