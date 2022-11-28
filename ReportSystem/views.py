from django.shortcuts import redirect, render
from django.db.models import Q
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from ReportSystem.forms import UserForm
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Create your views here.
def index(request):
    return render(request,'index.html')

class LoginView(View):
    
    def get(self,request):
        form = UserForm()
        if "sign-in" in request.GET:
            username = request.GET.get("username")
            password = request.GET.get("pswd")
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                messages.info(request,'Login attemp failed.')
                return redirect('account_login')
        return render(request,'login.html',{'form':form})
    
    def post(self,request):
        if "sign-up" in request.POST:
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                selected_group = request.POST.get("groups")
                group, created = Group.objects.get_or_create(name=selected_group)
                user.groups.add(group)
                messages.success(request,'Account has been created succesfully')
                return redirect('account_login')
            else:
                messages.error(request,form.errors)
                return redirect('account_login')
        return render(request,'login.html')

class LogoutView(View):

    def get(self,request):
        logout(request)
        messages.success(request,'Logged out succesfully.')
        return redirect('account_login')

def status(request):
    return render(request, 'viewStatusDetails.html')

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