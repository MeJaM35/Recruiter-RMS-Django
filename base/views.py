from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import User, Applicant, Skill, Edu, Exp, Organization, Recruiter, Job, Application
from .forms import UserSignUpForm, ApplicantForm, ProfileForm, EduForm, ExpForm, OrgForm, AdminForm, RecruiterForm, JobForm
from django.contrib import messages
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect 
from django.core.mail import EmailMessage, get_connection
from datetime import datetime


def convert_cgpa_to_percentage(cgpa):
    percentage = cgpa * 9.5
    return percentage


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Applicant

class PDFView(View):
    def get(self, request, pk):
        # Retrieve the Applicant instance
        applicant = get_object_or_404(Applicant, id=pk)

        # Retrieve the file path of the resume field
        resume_file_path = applicant.resume.path

        # Open the resume file in binary mode
        with open(resume_file_path, 'rb') as resume_file:
            # Read the file content
            resume_content = resume_file.read()

            # Create an HttpResponse object with the resume content
            response = HttpResponse(resume_content, content_type='application/pdf')

            # Add the Content-Disposition header to indicate inline display
            response['Content-Disposition'] = 'inline; filename=my_resume.pdf'

            return response




def register_org(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = OrgForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            org = form.save()
            return redirect('register-admin', org.id)

    context = {
        'form' : form,
    }

    return render(request, 'base/org_create.html', context)


def register_admin(request,pk):
    form = AdminForm(request.POST)
    if request.user.is_authenticated:
        return redirect('home')
    org = Organization.objects.get(id=pk)
    if form.is_valid():
            user = form.save(commit=False)
            user.role = 'admin'
            user.email = org.email
            user.username = org.name+"_admin"
            user.save()
            org.admin = user
            org.is_activated = True
            org.save()
            login(request, user)
            return redirect('home')
            

    context = {
       'form': form,
    }

    return render(request, 'base/admin-register.html', context)


@login_required(login_url='login')
def add_recruiter(request):
    Org = Organization.objects.get(admin=request.user)
    if request.user.role == 'admin':
        form = RecruiterForm(request.POST)
        if request.method == 'POST':        # For 'POST' request
            form = RecruiterForm(request.POST)
            if form.is_valid():
                rec = form.save(commit=False)
                rec.role = 'recruiter'
                rec.save()
                recu = Recruiter.objects.create(
                    User = rec,
                    role = 'recruiter',

                )
                Org.recruiters.add(recu)
                return redirect('home')
                
                # connection = get_connection()
                # with connection as connection:

                #     message = '''
                #             Hey {rec.User.username}, here's your {rec.User.org} Recruiter
                #             Use your email with password: {request.POST.get('password1')}
                #             '''
                #     Email = EmailMessage('Heres your email',message,'mj@sertibots.com',rec.email,connection=connection)
                #     Email.send()
                #     connection.close()
                
                

    context  = {
        'form': form,
    }

    return render(request, 'base/add-recruiter.html', context)






def register(request):
    form = UserSignUpForm()
    if request.method == 'POST':        # For 'POST' request
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'applicant'
            user.save()
            login(request, user)
            messages.success(
                request, f'Your account has been created! You are now logged in!')
            if user.role == 'applicant':
                return redirect('applicant-edit')
        else:
            form = UserSignUpForm(request.POST)
            messages.error(request, 'An error occurred during registration')
            return redirect('register')
    else:                            # Else for 'GET' request
        form = UserSignUpForm()
    context = {
        'form' : form,
    }
    return render(request, 'base/register.html', context)



        
    


@login_required(login_url='login')
def view_profile(request, pk):
    user = User.objects.get(id=pk)
    Skills = Skill.objects.filter(applicant = user.applicant)
    edu = Edu.objects.filter(applicant = user.applicant)
    exp = Exp.objects.filter(applicant = user.applicant)
    
    context = {
        'User' : user,
        'Skills' : Skills,
        'Edu' : edu,
        'exp': exp,

    }
    return render(request, 'base/applicant-details.html', context)


@login_required(login_url='login')
def add_edu(request):
    User =request.user
    edu = Edu.objects.filter(applicant = User.applicant)
    form = EduForm(request.POST)
    if request.method == 'POST':
       edu = form.save()
       User.applicant.edu.add(edu)


       return redirect('view-profile', User.id)
   

        


    context = {
        'User': User,
        'form': form,
        'edu': edu,
    }
    return render(request, 'base/add-edu.html', context)


@login_required(login_url='login')
def add_exp(request):
    User =request.user
    exp = Exp.objects.filter(applicant = User.applicant)
    form = ExpForm(request.POST)
    if request.method == 'POST':
       exp = form.save()
       User.applicant.exp.add(exp)


       return redirect('view-profile', User.id)
   

        


    context = {
        'User': User,
        'form': form,
        'exp': exp,
    }
    return render(request, 'base/add-exp.html', context)

@login_required(login_url='login')
def add_skills(request):
    page = 'add_skill'
    User =request.user
    Skills = Skill.objects.filter(applicant = User.applicant)
    if request.method == 'POST':
        skill, created = Skill.objects.get_or_create(name=request.POST.get('name'))
        User.applicant.skills.add(skill)


        return redirect('view-profile', User.id)
   

        


    context = {
        'User': User,
        'Skills': Skills,
    }
    return render(request, 'base/add-skills.html', context)

@login_required(login_url='login')
def user_edit(request, pk):
    user = User.objects.get(id=pk)
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view-profile', user.id)
   

        


    context = {
        'pform': form,
    }
    return render(request, 'base/user-edit.html', context)

@login_required(login_url='login')
def applicant_edit(request):
    User = request.user

    # Get the existing applicant object for the logged-in user
    try:
        applicant = Applicant.objects.get(User=User)
    except Applicant.DoesNotExist:
        applicant = None

    if request.method == 'POST':
        # If the form is submitted, update or create the applicant object
        form = ApplicantForm(request.POST, instance=applicant)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.User = User
            applicant.save()
            return redirect('view-profile', User.id)
    else:
        # If it's a GET request, create a form with initial data from the applicant object
        form = ApplicantForm(instance=applicant)

    context = {
        'form': form,
        'User': User,
    }
    return render(request, 'base/applicant-edit.html', context)

          


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    user = request.user
    context = {
        'user': user,
    }
    if user.is_authenticated:
        
        if user.role == 'applicant':
            job = Job.objects.filter(is_active = True)
            context['job'] = job
        if user.role == 'recruiter':
            job = Job.objects.filter(Recruiter = user.recruiters )
            context['job'] = job
        if user.role == 'admin':
            recruiter = Organization.objects.filter(admin=user)
            context['recruiter'] = recruiter
            
    else:
        job = Job.objects.all()
        context['job'] = job

    
    
    return render(request, 'base/home.html', context) 




@login_required(login_url='login')
def jobdetails(request,pk):
    user = request.user
    if user.role == 'recruiter':
        job = Job.objects.get(id = pk)
        apps = Application.objects.filter(job=job)

    context = {
        'apps' : apps,
    }

    return render(request, 'base/job-details.html', context)

@login_required(login_url='login')
def closejob(request, pk):
    user = request.user
    if user.role == 'recruiter':
        job = Job.objects.get(id = pk)
        job.is_active = False
        job.save()
        return redirect(request.META.get('HTTP_REFERER')) 
    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def activatejob(request, pk):
    user = request.user
    if user.role == 'recruiter':
        job = Job.objects.get(id = pk)
        job.is_active = True
        job.save()
        return redirect(request.META.get('HTTP_REFERER')) 
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def shortlist(request, pk):
    user = request.user
    context = {'user': user}
    if user.role == 'recruiter':
        app = Application.objects.get(id=pk)
        app.status = "shortlisted"
        app.save()
        context['app'] = app
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def accept(request, pk):
    user = request.user
    context = {'user': user}
    if user.role == 'recruiter':
        app = Application.objects.get(id=pk)
        if app.status == 'interviewed':
            app.status = "accepted"
            app.save()
            context['app'] = app
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))




@login_required(login_url='login')
def reject(request, pk):
    user = request.user
    context = {'user': user}
    if user.role == 'recruiter':
        app = Application.objects.get(id=pk)
        if app.status == 'interviewed':
            app.status = "rejected"
            app.save()
            context['app'] = app
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def interview(request, pk):
    user = request.user
    context = {'user': user}
    if user.role == 'recruiter':
        app = Application.objects.get(id=pk)
        
        app.status = "interviewed"
        app.save()
        context['app'] = app
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))










@login_required(login_url='login')
def addJob(request):
    User = request.user
    print(User.recruiters.org)
    form = JobForm()

    if request.method == 'POST':
        # print('post request')
        # if form.is_valid():
            print('post request')
            job = Job.objects.create(
                Org = Organization.objects.get(recruiters = User.recruiters),
               Recruiter = User.recruiters,
                position = request.POST.get('position'),
                start_date = request.POST.get('start_date'),
                pay_range = request.POST.get('pay_range'),
                description = request.POST.get('description'),
               


            )
            
            
            return redirect('home')

    context = {
        'form': form,
    }


    return render(request, 'base/add-job.html', context)
# Create your views here.

def chat(request):
    return render(request, "base/chat.html")

def room(request, room_name):
    return render(request, "base/chat-room.html", {"room_name": room_name})

def contact(request):
   
    return render(request, 'base/contact.html', context={}) 

def about(request):
    return render(request, 'base/about.html', context={}) 



@login_required(login_url='login')
def notif(request):
    user = request.user
    context = {}
    if user.role == 'applicant':
        App = Application.objects.filter(applicant = user.applicant)
        context['app'] = App

    
   
    return render(request, 'base/notif.html', context)



@login_required(login_url='login')
def Apply(request, pk):
    user = request.user
    job = Job.objects.get(id=pk)
    if user.role == 'applicant':
        application = Application.objects.create(
            job = job,
            applicant = user.applicant,
            status = 'applied',
        )
        return redirect('notif')
    return render(request, 'base/apply.html')
