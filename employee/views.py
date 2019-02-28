from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from employee.models import department, staff, project, leave, manager, employee, time_sheet, project_assingment
from django.db.models import Q,Subquery
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import datetime

# Index Page view


def index(request):
    
    emp = staff.objects.all().count()
    p = project.objects.filter(project_status='complete').count()
    return render(request, 'employee/index.html', {'emp1': emp, 'no_of_project': p})
    

# # All department view


def departments(request):
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
    d = request.session.get('dept')
    if request.method == 'POST':
        name = request.POST.get('search')
        st = employee.objects.filter(Q(staff__first_name__contains=name) | Q(
            staff__last_name__istartswith=name) | Q(staff__dept__dept_name__istartswith=name))
        context_dict = {'employees': st}

        return context_dict
    else:

        employee_list = employee.objects.order_by('-id')
        context_dict = {'employees': employee_list}

    return render(request, 'employee/employee_list.html', context_dict)


#  login view
def login(request):

    uname = ''
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
            return HttpResponse("User is not registered")
    return render(request, 'employee/login.html', {})


def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect('index')


def edit_employee(request, eid):
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
        print('done')

        return redirect('employees_list')
    return render(request, 'employee/edit.html', {'emp': s})


def delete_employee(request, eid):
    e = staff.objects.get(id=eid)
    e.delete()
    return redirect('employees_list')


def leave_request(request):
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
    did = request.session.get('dept')
    eid = request.session.get('user')
    leaves = leave.objects.filter(~Q(staff_id=eid), dept=did)
    context_dict = {'leaves': leaves}
    return render(request, 'employee/show_leaves.html', context_dict)


def approve(request, lid):
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
    l = leave.objects.filter(id=lid)
    if request.method == "POST":
        le = leave.objects.get(id=lid)
        le.leave_status = 'Deny'
        le.save()
        return redirect('show_leaves')
    return render(request, 'employee/show_leaves.html')


def profile(request):
    uid = request.session.get('user')
    st = staff.objects.filter(id=uid)
    return render(request, 'employee/profile.html', {'emp': st})


def projects(request):
    project_list = project_assingment.objects.all()
    eid = request.session.get('user')
    p1 = ''
    print(eid)
    for p in project_list:
        if p.emp.staff_id == eid:
            print(p.emp.staff_id)
            p1 = project_assingment.objects.filter(emp__staff_id=eid)
            for p in p1:
                print(p.emp.staff_id)
    context_dict = {'projects': p1}
    return render(request, 'employee/project_list.html', context_dict)


def add_project(request):
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
        # subject = 'You have got a new project'
        # message = 'Project Details: ' + '\nProject Name:  '+ p.project_name + '\nProject Technology: '+ p.project_technology + '\nProject Start Date: '+ p.project_start_date + '\nProject End Date: '+ p.project_end_date
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [p.staff.email,]
        # send_mail(subject,message,email_from,recipient_list)
        return redirect('all_projects')

    return render(request, 'employee/add_project.html', {'dept': dept})


def all_projects(request):
    if request.method == 'POST':
        name = request.POST.get('search')
        project_list = project.objects.filter(project_name__istartswith=name)
        context_dict = {'projects': project_list}
    else:
        project_list = project.objects.filter()
        context_dict = {'projects': project_list}
    return render(request, 'employee/all_projects.html', context_dict)


def manager_list(request):
    manage = manager.objects.all()
    return render(request, 'employee/manager_list.html', {'employees': manage})

#  def help_desk(request):
#     return render(request,'employee/help_desk.html', {})

# def demo(request):
#     return render(request,'employee/demo.html', {})


def complete(request, pid):
    if request.method == "POST":
        pr = project.objects.get(id=pid)
        print(pid)
        pr.project_status = 'complete'
        pr.save()
        return redirect('all_projects')
    return render(request, 'employee/all_projects.html')


def updates(request):
    return render(request, 'employee/updates.html', {})


def timesheet(request):
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

    st = employee.objects.all()
    pr = project.objects.all()
    msg = ''
    if request.method == "POST":
        p = project_assingment()
        print(request.POST.get('pid'))

        st = employee.objects.get(staff_id=request.POST.get('emp'))
        pr = project.objects.get(id=request.POST.get('pid'))
        # print(request.POST.get('emp'))

        p.emp = st
        p.project = pr
        p.save()
        msg = 'The project has been assigned Successfully...'
        subject = 'You have got a new project'
        message = 'Project Details: ' + '\nProject Name:  ' + p.project.project_name + '\nProject Technology: ' + p.project.project_technology + '\nProject Start Date: ' + str(p.project.project_start_date) + '\nProject End Date: ' + str(p.project.project_end_date)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [p.emp.staff.email,]
        send_mail(subject,message,email_from,recipient_list)
        return render(request, 'employee/assign_project.html', {'msg': msg})
    return render(request, 'employee/assign_project.html', {'staff': st, 'project': pr, 'msg': msg})


def abc(request):
    val = request.GET['value']
    if val == 'assign':
        pr = project.objects.filter(id__in=Subquery(project_assingment.objects.all().values('project'))) 
    elif val == 'unassign':
        pr = project.objects.filter(~Q(id__in=Subquery(project_assingment.objects.all().values('project')))) 
    return render(request,'employee/assign.html', {'projects':pr})   
