from django.db import models

# Create your models here.
class Team(models.Model):
    teamName = models.CharField(max_length=100,null=True)
    teamLeaderName = models.CharField(max_length=100,null=True)
    teamMobno = models.CharField(max_length=20,null=True)
    teamMembers = models.CharField(max_length=200,null=True)
    postingDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.teamName

class Fraudreport(models.Model):
    fullName = models.CharField(max_length=100,null=True)
    mobileNumber = models.CharField(max_length=20,null=True)
    location = models.CharField(max_length=200,null=True)
    message = models.CharField(max_length=200,null=True)
    assignTo = models.ForeignKey(Team,on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=200,null=True)
    postingDate = models.DateTimeField(auto_now_add=True)
    assignedTime = models.CharField(max_length=200,null=True)
    updationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullName    

class ReportHistory(models.Model):
    fraudreport = models.ForeignKey(Fraudreport,on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=200,null=True)
    remark = models.CharField(max_length=200,null=True)
    postingDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status    
