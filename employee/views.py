from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from employee.models import department, staff, project, leave, manager, employee, time_sheet, project_assingment,project_inquiry
from django.db.models import Q,Subquery
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.conf import settings
import datetime
from django.urls import reverse
from django.contrib.auth.hashers import make_password
# Index Page view


def index(request):
    ''' Index Page '''
    context_dict = {}
    sid = request.session.get('user')
    role = request.session.get('type')
    did = request.session.get('dept')
    if role == 'manager':
        pl = leave.objects.filter(~Q(staff_id=sid), dept=did, leave_status='').count()
        up = project.objects.filter(~Q(id__in=Subquery(project_assingment.objects.all().values('project'))),dept=did).count()
        ap = project.objects.filter(id__in=Subquery(project_assingment.objects.all().values('project')),dept=did).count()
        emp = employee.objects.filter(staff__dept=did).count()
        unass_pr = project.objects.filter(
            ~Q(id__in=Subquery(project_assingment.objects.all().values('project'))))
       
        pinquiry = project_inquiry.objects.filter(~Q(staff_id=sid),staff__dept_id=did,reply='no').order_by('-id')
        context_dict = {'pending_leaves':pl,'unassign_projects':up,'assigned_projects':ap,'total_employees':emp,'unass_pr':unass_pr,'pinquiry':pinquiry} 
    elif role == 'employee':
        pl = leave.objects.filter(Q(staff_id=sid), dept=did, leave_status='').count()
        ap = project_assingment.objects.filter(emp__staff_id=sid).count()
        cp = project_assingment.objects.filter(Q(emp__staff_id=sid),project__dept=did ,status='complete').count()
        ap1 = project.objects.filter(id__in=Subquery(project_assingment.objects.all().values('project')),dept=did).count()
       
        tl = leave.objects.filter(Q(staff_id=sid), dept=did, leave_status='Approve').count()
        pinquiry = project_inquiry.objects.filter(~Q(staff_id=sid),staff__dept_id=did,reply='no',project=ap1).order_by('-id')
       
        context_dict = {'pending_leaves':pl,'assigned_projects':ap,'complete_projects':cp,'total_leaves':tl,'pinquiry':pinquiry}
    return render(request, 'employee/index.html', context_dict)
    

# # All department view


def departments(request):
    ''' Display Department Details and Total number of employees
    in each Department '''
    if request.method == 'POST':
        name = request.POST.get('search')
        departments = department.objects.filter(dept_name__istartswith=name)

        dict1 = {}
        for d in departments:
            if d.dept_name not in dict1:
                c = 0
                c = staff.objects.filter(dept_id=d.id).count()
                dict1[d.dept_name] = c
    else:
        departments = department.objects.all()
        st = staff.objects.all()
        dict1 = {}
        for d in departments:
            if d.dept_name not in dict1:
                c = 0
                c = staff.objects.filter(dept_id=d.id).count()
                dict1[d.dept_name] = c
    return render(request, 'employee/department_list.html', {'dict1': dict1})

# # Showing all the employee details


def employee_register(request):
    ''' Function to add employee details '''
    dept = department.objects.all()
    if request.method == 'POST':
        d = department.objects.get(dept_name=request.POST.get('dept'))
        s = staff.objects.create(first_name=request.POST.get('fname'),
                                 email=request.POST.get('email'),
                                 last_name=request.POST.get('lname'),
                                 gender=request.POST.get('gender'),
                                 date_of_birth=request.POST.get('dob'),
                                 password=request.POST.get('password'),
                                 phone_no=request.POST.get('phone_no'),
                                 address=request.POST.get('address'),
                                 city=request.POST.get('city'),
                                 qualification=request.POST.get(
                                     'qualification'),
                                 designation=request.POST.get('designation'),
                                 skills=request.POST.get('skills'),
                                 experience=request.POST.get('experience'),
                                 date_of_joining=request.POST.get('doj'),
                                 salary=request.POST.get('salary'),
                                 profile_image=request.FILES.get(
                                     'profile_image'),
                                 dept=d)

        s.save()
        e = employee.objects.create(staff=s)
        e.save()

        subject = 'Employee Management System'
        message = 'Username:  '+e.staff.email + '\nPassword: ' + e.staff.password
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e.staff.email, ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect('employees_list')
    return render(request, 'employee/employee_register.html', {'dept': dept})


def employees(request):
    ''' Display Employee details '''
    d = request.session.get('dept')
    if request.method == 'POST':
        name = request.POST.get('search')
        st = employee.objects.filter(Q(staff__first_name__contains=name) | Q(
            staff__last_name__istartswith=name) | Q(staff__dept__dept_name__istartswith=name))
        context_dict = {'employees': st}

        return context_dict
    else:
        dept = department.objects.all()
        employee_list = employee.objects.order_by('-id')
        context_dict = {'employees': employee_list,'dept':dept}

    return render(request, 'employee/employee_list.html', context_dict)


#  login view
def login(request):
    ''' Login Function '''
    uname = ''
    msg = ''
    if request.method == 'POST':
        uname = request.POST.get('email')
        password = request.POST.get('password')
        try:
            member = staff.objects.get(email=uname, password=password)
            try:
                user = employee.objects.get(staff=member)

                request.session['user'] = member.id
                request.session['type'] = 'employee'
                request.session['dept'] = member.dept.id
                request.session['image'] = str(member.profile_image)
                request.session['fname'] = member.first_name
                request.session['lname'] = member.last_name
                return redirect('index')
                # return HttpResponse("User is Employee")
            except:
                try:
                    user = manager.objects.get(staff=member)
                    request.session['user'] = member.id
                    request.session['dept'] = member.dept.id
                    request.session['image'] = str(member.profile_image)
                    request.session['type'] = 'manager'
                    request.session['fname'] = member.first_name
                    request.session['lname'] = member.last_name
                    return redirect('index')
                    # return HttpResponse("User is manager")
                except:
                    return HttpResponse('user is registered but not employeed')
        except Exception as e:
            print('error ', e)
            msg = 'Invalid Email and Password'
    return render(request, 'employee/login.html', {'msg':msg})


def logout(request):
    ''' Logout Function '''
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect('index')



def edit_employee(request, eid):
    ''' Function to add employee details '''
    s = staff.objects.filter(id=eid)
    if request.method == 'POST':

        s = staff.objects.get(id=eid)
        s.first_name = request.POST.get('fname')
        s.last_name = request.POST.get('lname')
        s.phone_no = request.POST.get('phone_no')
        s.address = request.POST.get('address')
        s.city = request.POST.get('city')
        s.designation = request.POST.get('designation')
        s.skills = request.POST.get('skills')
        s.experience = request.POST.get('experience')
        if request.FILES.get('profile_image'):
            s.profile_image = request.FILES.get('profile_image')

        s.salary = request.POST.get('salary')
        s.save()
        e = employee.objects.get(staff_id=eid)
        e.save()
        


        return redirect('employees_list')
    return render(request, 'employee/edit.html', {'emp': s})


def delete_employee(request, eid):
    ''' Function to delete employee details '''
    e = staff.objects.get(id=eid)
    e.delete()
    return redirect('employees_list')


def leave_request(request):
    ''' Function to apply leave request '''
    eid = request.session.get('user')
    st = staff.objects.get(id=eid)
    emp_leave = leave.objects.filter(staff=eid)
    msg = ''
    if request.method == "POST":

        l = leave()
        l.dept_id = request.POST.get('dept_id')
        l.staff_id = request.POST.get('emp_id')
        l.leave_date = request.POST.get('leave_date')
        l.leave_time = request.POST.get('leave_time')
        l.leave_reason = request.POST.get('leave_reason')

        l.save()
        msg = 'Your Leave Request has been sent Successfully...'

    return render(request, 'employee/leave_request.html', {'dname': st.dept, 'ename': st.first_name, 'elname': st.last_name, 'dept_id': st.dept_id, 'emp_id': st.id, 'emp_leave': emp_leave, 'msg': msg})


def show_leaves(request):
    ''' Function to display leave details '''
    did = request.session.get('dept')
    eid = request.session.get('user')
    leaves = leave.objects.filter(~Q(staff_id=eid), dept=did)
    context_dict = {'leaves': leaves}
    return render(request, 'employee/show_leaves.html', context_dict)


def approve(request, lid):
    ''' Function to approve leaves of an employee '''
    e = employee.objects.all()
    if request.method == "POST":
        le = leave.objects.get(id=lid)
        le.leave_status = 'Approve'
        le.save()
        subject = 'Your leave has been approved'
        message = 'Leave Details:' + '\nLeave date:  ' + \
            str(le.leave_date) + '\nLeavev reason: ' + \
            le.leave_reason + '\nLeave time: ' + le.leave_time
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [le.staff.email, ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect('show_leaves')
    return render(request, 'employee/show_leaves.html')


def deny(request, lid):
    ''' Function to deny leave of employee '''
    l = leave.objects.filter(id=lid)
    if request.method == "POST":
        le = leave.objects.get(id=lid)
        le.leave_status = 'Deny'
        le.save()
        subject = 'Your leave has been rejected'
        message = 'Leave Details:' + '\nLeave date:  ' + \
            str(le.leave_date) + '\nLeavev reason: ' + \
            le.leave_reason + '\nLeave time: ' + le.leave_time
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [le.staff.email, ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect('show_leaves')
    return render(request, 'employee/show_leaves.html')


def profile(request):
    ''' Display User Profile '''
    uid = request.session.get('user')
    st = staff.objects.filter(id=uid)
    return render(request, 'employee/profile.html', {'emp': st})


def projects(request):
    ''' Display Project Details '''
    project_list = project_assingment.objects.all()
    eid = request.session.get('user')
    p1 = ''
    
    for p in project_list:
        if p.emp.staff_id == eid:
            p1 = project_assingment.objects.filter(emp__staff_id=eid).order_by('-id')            
    context_dict = {'projects': p1}
    return render(request, 'employee/project_list.html', context_dict)


def add_project(request):
    ''' Function to add project details '''
    dept = department.objects.all()
    if request.method == "POST":
        # d = department.objects.get(dept_name=request.POST.get('dept'))
        # p.dept = d
        # p.staff_id = request.POST.get('emp')
        p = project()
        d = department.objects.get(dept_name=request.POST.get('dept'))
        p.dept = d
        p.project_name = request.POST.get('pname')
        p.project_start_date = request.POST.get('psdate')
        p.project_end_date = request.POST.get('pedate')
        p.project_technology = request.POST.get('ptech')
        p.save()
        return redirect('all_projects')

    return render(request, 'employee/add_project.html', {'dept': dept})


def all_projects(request):
    ''' search employees '''
    if request.method == 'POST':
        name = request.POST.get('search')
        project_list = project.objects.filter(project_name__istartswith=name)
        context_dict = {'projects': project_list}
    else:
        project_list = project.objects.filter()
        context_dict = {'projects': project_list}
    return render(request, 'employee/all_projects.html', context_dict)


def manager_list(request):
    ''' Display Manager Details '''
    manage = manager.objects.all()
    return render(request, 'employee/manager_list.html', {'employees': manage})

#  def help_desk(request):
#     return render(request,'employee/help_desk.html', {})

# def demo(request):
#     return render(request,'employee/demo.html', {})


def complete(request, pid):
    ''' Display Completed Projects  '''
    if request.method == "POST":
        pr = project.objects.get(id=pid)
      
        pr.project_status = 'complete'
        pr.save()
        return redirect('all_projects')
    return render(request, 'employee/all_projects.html')


def updates(request):
    return render(request, 'employee/updates.html', {})


def timesheet(request):
    ''' Add Timesheet  '''
    st = staff.objects.all()
    pr = project_assingment.objects.all()
    now = datetime.datetime.now()
    now1 = now.strftime("%Y-%m-%d")
    time = time_sheet.objects.all()
    if request.method == 'POST':
        p = project.objects.get(id=request.POST.get('project'))
        s = staff.objects.get(first_name=request.POST.get('emp_name'))

        t = time_sheet()
        t.staff = s
        t.pid = p
        t.date = request.POST.get('date')
        t.time = request.POST.get('hours')
        t.description = request.POST.get('description')
        t.save()
        return redirect('time_sheet')

    return render(request, 'employee/time_sheet.html', {'staff': st, 'now': now1, 'project': pr, 'time_sheet': time})


# def project_info(request):

#     return render(request, 'employee/project_info.html', {})

def assign_project(request):
    ''' Assign Project to an Employee'''
    st = employee.objects.all()
    pr = project.objects.all()
    msg = ''
    
    if request.method == "POST":
        p = project_assingment()
       

        st = employee.objects.get(staff_id=request.POST.get('emp'))
        pr = project.objects.get(id=request.POST.get('pid'))
        
       
        try:
            p = project_assingment.objects.get_or_create(emp=st,project=pr)
            
        except Exception as e:
            print(e)
     
        p1 = project_assingment.objects.order_by('-id')[:1]
        for e in p1:
            pname = e.project.project_name
            emp = e.emp.staff.email
            sdate = str(e.project.project_start_date)
            edate = str(e.project.project_end_date)
            ptech = e.project.project_technology
     
        msg = 'The project has been assigned Successfully...'
        subject = 'You have got a new project'
        message = 'Project Details: ' + '\nProject Name:  ' + pname +  '\nProject Start Date: ' + sdate + '\nProject End Date: ' + edate + '\nProject Technology: ' + ptech 
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [emp,]
        send_mail(subject,message,email_from,recipient_list)
        # p.emp = st
        # p.project = pr
        # p.save()
        # msg = 'The project has been assigned Successfully...'
        # subject = 'You have got a new project'
        # message = 'Project Details: ' + '\nProject Name:  ' + p1.project 
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [p1.emp.staff.email,]
        # send_mail(subject,message,email_from,recipient_list)
        return redirect('assign_project')
    return render(request, 'employee/assign_project.html', {'staff': st, 'project': pr, 'msg': msg})

def abc(request):
    val = request.GET['value']
    if val == 'assign':
        pr = project.objects.filter(id__in=Subquery(
            project_assingment.objects.all().values('project')))
        return render(request, 'employee/assign.html', {'projects': pr})
    elif val == 'unassign':
        pr = project.objects.filter(
            ~Q(id__in=Subquery(project_assingment.objects.all().values('project'))))
        return render(request, 'employee/unassign.html', {'projects': pr})   


def holiday(request):
    ''' Display Holiday List '''
    return render(request,'employee/holiday.html')

def leave_format(request):
    ''' Display Leave Applying Format '''
    return render(request,'employee/leave_format.html')

def update_mail(request):
    ''' Display Mail Applying Format '''
    return render(request,'employee/update_mail.html')

def policy(request):
    ''' Display Compnay Details '''
    return render(request,'employee/policy.html')


def help_desk(request):
    ''' Helpdisk For User '''
    return render(request,'employee/help_desk.html', {})

def base1(request):
    return render(request,'employee/base1.html', {})

def change_password(request):
    ''' Allow Login User to change password  '''
    eid = request.session.get('user')
    old = request.POST.get('oldpassword')
    new = request.POST.get('newpassword')
    new1 = request.POST.get('newpassword2')
    c1 = staff.objects.filter(id=eid)
    msg =''
    if request.method == 'POST':
        if new == new1:
          
            c1 = staff.objects.get(id=eid)
            if c1.password == old:
               
                c1.password = request.POST.get('newpassword2')
                c1.save()  

                msg = 'Password has been change  suceesfully....'
                subject = 'Employee Management System'
                message = 'Your Password has been change successfully'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [c1.email,]
                send_mail(subject,message,email_from,recipient_list)
                
        else:
            msg = "New Password and Re-enter Password must be same."
    return render(request,'employee/change_password.html',{'msg':msg})

def project_info(request):
    val = request.GET['value']
    employee_info = project_assingment.objects.filter(project_id=val)
    return render(request, 'employee/project_info.html', {'employee_info':employee_info})



def filter_by_dept(request):
    val = request.GET['value']
    if val != '':
        try:
            emp = employee.objects.filter(staff__dept_id=val)           
        except:      
            return HttpResponse('Something went wrong with ajax..')       
    return render(request, 'employee/filter_by_dept.html', {'employee': emp})

def inquiry(request):
    
    sid = request.session.get('user') 
    manager = request.session.get('type')
    if manager == 'manager':
        dept = request.session.get('dept')
        proj = project.objects.filter(dept_id=dept)
        st = staff.objects.filter(id=sid)
        now = datetime.datetime.now()
        now1 = now.strftime("%Y-%m-%d, %H:%M:%S %p")
        p1 = project_inquiry.objects.all().order_by('-id')
        context_dict = {'project': proj, 'staff': st, 'now': now1,'project_inquiry':p1}
    else:
        pr = project_assingment.objects.filter(emp__staff_id=sid)
        print(pr.values())
        st = staff.objects.filter(id=sid)
        now = datetime.datetime.now()
        now1 = now.strftime("%Y-%m-%d, %H:%M:%S %p")
        p1 = project_inquiry.objects.all().order_by('-id')[:8]
        context_dict = {'project': pr, 'staff': st, 'now': now1,'project_inquiry':p1}
    
    if request.method == 'POST':
        print('hii~~~~~~~~~~~~>')
        pi = project_inquiry()
        # if manager == 'employee':
        #     # pr1 = project_assingment.objects.get(id=request.POST.get('project'))
        #     pr1 = project_assingment.objects.get(id=request.POST.get('project'))
        # elif manager == 'manager':
        
        pr1 = project.objects.get(id=request.POST.get('project'))
        print(pr1)

        try:
            pi.project = pr1
            st1 = staff.objects.get(id=request.POST.get('ename'))
            pi.staff = st1
            pi.time = request.POST.get('time')
            pi.comment = request.POST.get('comment')
           
            pi.save()
            
        except Exception as e:
            print("Something wrong while adding query.", e)

    return render(request, 'employee/project_inquiry.html', context_dict)

def project_complete(request,pid):
    if request.method == "POST":
        pr = project_assingment.objects.get(id=pid)
  
        pr.status = 'complete'
        pr.save()
        return redirect('projects')
       
    return render(request, 'employee/project_list.html',{})

def project_inprogress(request,pid):
    if request.method == "POST":
        pr = project_assingment.objects.get(id=pid)
  
        pr.status = 'inprogress'
        pr.save()
        return redirect('projects')
       
    return render(request, 'employee/project_list.html',{})

def reply(request,pid):
    # if request.method == 'POST':
    pi = project_inquiry.objects.get(id=pid)
    pi.reply = 'yes'
    pi.save()
    return redirect('project_inquiry')