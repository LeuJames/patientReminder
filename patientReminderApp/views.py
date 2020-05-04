from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt, datetime

def index(request):
    return redirect('/ptLogReg')

def ptLogReg(request):
    context = {
        'allPhys' : Physician.objects.all()
    }
    return render(request, 'ptLogReg.html', context)

def physLogReg(request):
    return render(request, 'physLogReg.html')

def ptDashboard(request):
    if 'ptID' in request.session:
        pt=Patient.objects.get(id=request.session['ptID'])
        ptTasks = pt.tasks.exclude(status="Completed")
        for x in ptTasks:
            if x.status == 'Upcoming' and x.date < datetime.date.today():
                x.status = 'Due'
                x.save()
        context = {
            'pt' : pt,
            'ptTasks' : ptTasks.order_by('date'),
        }
        return render(request, 'ptDashboard.html', context)
    return redirect ('/ptLogReg')

def physDashboard(request):
    if 'physID' in request.session:
        phys = Physician.objects.get(id=request.session['physID'])
        physTasks = phys.tasks.exclude(status="Completed")
        for x in physTasks:
            if x.status == 'Upcoming' and x.date < datetime.date.today():
                x.status = 'Due'
                x.save()
        context = {
            'phys' : phys,
            'physPts' : phys.patients.all(),
            'physTasks' :physTasks.order_by('date'),
        }
        request.session['currentRt'] = '/physDashboard'
        return render(request, 'physDashboard.html', context)
    return redirect ('/ptLogReg')

def newTask(request):
    if 'physID' in request.session:
        phys = Physician.objects.get(id=request.session['physID'])
        context = {
            'physPts' : phys.patients.all(),
            'physTasks' : phys.tasks.all().values_list('task', flat=True).distinct()
        }
        request.session['currentRt']='/newTask'
        return render(request, 'newTask.html', context)
    return redirect ('/ptLogReg')

def ptRegister(request):
    print(request.POST)
    errors = Patient.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/ptLogReg')
    password = request.POST['pw']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    newPt = Patient.objects.create(
        f_name=request.POST['f_name'],
        l_name=request.POST['l_name'],
        email=request.POST['email'],
        phys=Physician.objects.get(id=request.POST['phys']),
        password=pw_hash,
        dob=request.POST['dob']
        )
    request.session['ptID'] = newPt.id
    return redirect('/ptDashboard')

def ptLogin(request):
    errors = Patient.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='login')
            return redirect('/ptLogReg')
    request.session['ptID']=Patient.objects.get(email=request.POST['email']).id
    return redirect('/ptDashboard')

def ptLogout(request):
    request.session.clear()
    return redirect ('/ptLogReg')

def physRegister(request):
    errors = Physician.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/physLogReg')
    password = request.POST['pw']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    loggedPhys = Physician.objects.create(
        f_name=request.POST['f_name'],
        l_name=request.POST['l_name'],
        email=request.POST['email'],
        password=pw_hash,
        )
    request.session['physID'] = loggedPhys.id
    return redirect('/physDashboard')

def physLogin(request):
    errors = Physician.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='login')
            return redirect('/physLogReg')
    request.session['physID']=Physician.objects.get(email=request.POST['email']).id
    return redirect('/physDashboard')

def physLogout(request):
    request.session.clear()
    return redirect ('/physLogReg')

def createTask(request):
    if 'physID' in request.session:
        errors = Task.objects.task_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            request.session['lastRt']=request.session['currentRt']
            return redirect(request.session['lastRt'])
        if 'taskSelect' in request.POST:
            task = request.POST['taskSelect']
        else:
            task = request.POST['taskInput']
        newTask = Task.objects.create(
            task = task,
            desc = request.POST['desc'],
            pt = Patient.objects.get(id=request.POST['pt']),
            phys = Physician.objects.get(id=request.session['physID']),
            date = request.POST['date'],
            )
        request.session['lastRt']=request.session['currentRt']
        return redirect(request.session['lastRt'])
    return redirect ('/physLogReg')

def complete(request, taskID):
    if 'physID' in request.session:
        task = Task.objects.get(id=taskID)
        task.status = "Completed"
        task.save()
        request.session['lastRt']=request.session['currentRt']
        return redirect(request.session['lastRt'])
    return redirect ('/physLogReg')

def delete(request, taskID):
    if 'physID' in request.session:
        task = Task.objects.get(id=taskID)
        task.delete()
        request.session['lastRt']=request.session['currentRt']
        return redirect(request.session['lastRt'])
    return redirect ('/physLogReg')

def ptPage(request, ptID):
    if 'physID' in request.session:
        pt = Patient.objects.get(id=ptID)
        phys = Physician.objects.get(id=request.session['physID'])
        ptTasks = pt.tasks.exclude(status="Completed")
        for x in ptTasks:
            if x.status == 'Upcoming' and x.date < datetime.date.today():
                x.status = 'Due'
                x.save()
        context = {
            'pt' : pt,
            'ptTasks' : pt.tasks.filter(phys=phys).order_by('date'),
            'physTasks' : phys.tasks.all().values_list('task', flat=True).distinct()
        }
        request.session['currentRt'] = f'/patient/{ptID}'
        return render(request, "ptPage.html", context)
    return redirect ('/physLogReg')