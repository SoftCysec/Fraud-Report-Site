from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from ReportSystem import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index,name='index'),
    path("", views.LoginView.as_view(), name="account_login"),
    path('viewStatusDetails/', views.status,name='status'),
    path('reporting/', views.reporting,name='reporting'),
    path('viewStatus/', views.viewStatus,name='viewStatus'),
    path('admin_login/', views.admin_login,name='admin_login'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('logout/', views.Logout,name='logout'),
    path('addTeam/', views.addTeam,name='addTeam'),
    path('manageTeam/', views.manageTeam,name='manageTeam'),
    path('editTeam/<int:pid>/', views.editTeam,name='editTeam'),
    path('deleteTeam/<int:pid>/', views.deleteTeam,name='deleteTeam'),
    path('changePassword/', views.changePassword,name='changePassword'),
    path('search/', views.search,name='search'),
    path('allRequest/', views.allRequest,name='allRequest'),
    path('newRequest/', views.newRequest,name='newRequest'),
    path('assignRequest/', views.assignRequest,name='assignRequest'),
    path('teamontheway/', views.teamontheway,name='teamontheway'),
    path('workinprogress/', views.workinprogress,name='workinprogress'),
    path('completeRequest/', views.completeRequest,name='completeRequest'),
]+static(settings.MEDIA_URL,documentsroot=settings.MEDIA_ROOT)
