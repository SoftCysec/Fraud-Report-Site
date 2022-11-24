from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout

from . models import *
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request,'index.html')

def reporting(request):
    error = ""
    if request.method == 'POST':
        fullName = request.POST['FullName']
        mobileNumber = request.POST['MobileNumber']
        location = request.POST['Location']
        message = request.POST['Message']
        try:
            Fraudreport.objects.create(fullName=fullName,
                                        mobileNumber=mobileNumber,
                                        location=location,
                                        message=message)
            error = "no"                            
        except:
            error = "yes"
    return render(request,'reporting.html',locals())    

def viewStatus(request):
    sd = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
        try:
            fraudreport = Fraudreport.objects.filter(Q(fullName__icontains=sd) |
                                                 Q(mobileNumber__icontains=sd) | 
                                                 Q(location__icontains=sd))
        except:
            fraudreport = ""
    return render(request,'viewStatus.html',locals())

def admin_login(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        try:
            if user.is_staff:
                login(request,user)
                error = 'no'
        except:
            error = 'yes'        

    return render(request,'admin_login.html',locals())        

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin/dashboard.html', locals())  

def Logout(request):
    logout(request)
    return redirect('index')

def addTeam(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""        
    if request.method == "POST":
        teamName = request.POST['teamName']
        teamLeaderName = request.POST['teamLeaderName']
        teamLeadMobno = request.POST['teamLeadMobno']
        teamMembers = request.POST['teamMembers']
        try:
            Team.objects.create(teamName = teamName,
                                teamLeaderName = teamLeaderName, 
                                teamMobno = teamLeadMobno,
                                teamMembers = teamMembers)
            error = "no"                                    
        except:
            error = "yes"
    return render(request,'admin/addTeam.html',locals())    

def manageTeam(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    teams = Team.objects.all()    
    return render(request,'admin/manageTeam.html',locals())    

def editTeam(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    teams = Team.objects.get(id=pid)
    error =""
    if request.method == "POST":
        teamName = request.POST['teamName']
        teamLeaderName = request.POST['teamLeaderName']
        teamLeadMobno = request.POST['teamLeadMobno']
        teamMembers = request.POST['teamMembers']

        teams.teamName = teamName
        teams.teamLeaderName = teamLeaderName
        teams.teamMobno = teamLeadMobno
        teams.teamMembers = teamMembers

        try:
            teams.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/editTeam.html', locals())

def allRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    fraudreport = Fraudreport.objects.all()    
    return render(request,'admin/allRequest.html',locals())    

def deleteTeam(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    teams = Team.objects.get(id=pid)
    teams.delete()
    return redirect('manageTeam')

def newRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login') 
    fraudreport = Fraudreport.objects.filter(status__isnull=True)    
    return render(request,'admin/newRequest.html',locals())  

def assignRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login') 
    fraudreport = Fraudreport.objects.filter(status="Assigned")     
    return render(request,'admin/assignRequest.html',locals())   

def teamontheway(request):
    if not request.user.is_authenticated:
        return redirect('admin_login') 
    fraudreport = Fraudreport.objects.filter(status="Team On the Way")     
    return render(request,'admin/teamontheway.html',locals())  

def workinprogress(request):
    if not request.user.is_authenticated:
        return redirect('admin_login') 
    fraudreport = Fraudreport.objects.filter(status="Fraud Relief Work in Progress")     
    return render(request,'admin/workinprogress.html',locals())  

def completeRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login') 
    fraudreport = Fraudreport.objects.filter(status="Request Completed")     
    return render(request,'admin/assignRequest.html',locals())          

def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    user = request.user
    erro = ""    
    if request.method == "POST":
        oldpass = request.POST['oldpassword']
        newpass = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(oldpass):
                u.set_password(newpass)
                u.save()
                error = "no"
            else:
                error = "not"    
        except:
            error = "yes"
    return render(request,'admin/changePassword.html',locals())        

def search(reqeust):
    if not reqeust.user.is_authenticated:
        return redirect('admin_login')
    sd = None
    if reqeust.method == "POST":
        sd = reqeust.POST['searchdata']
        try:
            fraudreport = Fraudreport.objects.filter(Q(fullName__icontains=sd) |
                                                 Q(mobileNumber__icontains=sd) | 
                                                 Q(location__icontains=sd))
            error = "no"                                                     
        except:
            error = "yes"
    return render(reqeust,'admin/search.html',locals())    