from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('login', views.loginUser, name='login'),
    path('notifications', views.notif, name='notif'),
    path('<str:pk>/desc', views.desc, name='desc'),
    

    path('applicant/more-details', views.applicant_edit, name='applicant-edit'),
    path('applicant/more-details/add-skill', views.add_skills, name='add-skill'),
    path('applicant/more-details/add-education', views.add_edu, name='add-edu'),
    path('applicant/more-details/add-experience', views.add_exp, name='add-exp'),
    path('applicant/edit-details/<str:pk>/', views.user_edit, name='user-edit'),
    path('applicant/addLinks/', views.addLinks, name='add-links'),

    path('<str:pk>/view-profile', views.view_profile, name='view-profile'),

    path('organization/register', views.register_org, name='register-org'),
    path('organization/admin/register/<str:pk>', views.register_admin, name='register-admin'),
    path('organization/admin/add-recruiter/', views.add_recruiter, name='add-recruiter'),
    path('organization/admin/recruiter-details/<str:pk>', views.dashboard, name='recruiter-details'),
    path('organization/admin/recruiter-details/<str:pk>/<str:id>', views.get_apps, name='get-apps'),




    path('organization/recruiter/add-job/', views.addJob, name='add-job'),
    path('<str:pk>/apply', views.Apply, name='apply'),
    path('<str:pk>/close', views.closejob, name='close-job'),
    path('<str:pk>/activate', views.activatejob, name='activate-job'),
    path('<str:pk>/details', views.jobdetails, name='job-details'),
    path('<str:pk>/shortlist', views.shortlist, name='shortlist'),
    path('<str:pk>/interview', views.interview, name='interview'),
    path('<str:pk>/accept', views.accept, name='accept'),
    path('<str:pk>/reject', views.reject, name='reject'),

     path('pdf/<str:pk>/', views.PDFView.as_view(), name='pdf_view'),


    path('chat', views.chat, name='chat'),
    path("chat/<str:room_name>/", views.room, name="room"),



    path('contact',views.contact, name='contact'),
   
    path('about', views.about, name='about'),
    path('ERROR', views.ERROR, name='ERROR'),


]