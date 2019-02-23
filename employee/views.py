from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from employee.models import department, staff, project, leave, manager, employee
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# Index Page view


def index(request):
    # uname = request.session.get('uname')
    # e2 = employee.objects.filter(email=uname)
    # emp = employee.objects.all().count()
    # p = project.objects.filter(project_status='Complete').count()
    # return render(request, 'employee/index.html', {'emp': e2, 'emp1': emp,'no_of_project':p})
    return render(request, 'employee/index.html', {})

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
    # manage = manager.objects.all()
    # emp = employee.objects.all()
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
                return redirect('index')
                # return HttpResponse("User is Employee")
            except:
                try:
                    user = manager.objects.get(staff=member)
                    request.session['user'] = member.id
                    request.session['dept'] = member.dept.id
                    
                    request.session['type'] = 'manager'
                    return redirect('index')
                    # return HttpResponse("User is manager")
                except:
                    return HttpResponse('user is registered but not employeed')
        except Exception as e:
            print('error ', e)
            return HttpResponse("User is not registered")
        # for m in manage:

        #     if m.staff.email == uname and m.staff.password == password:
        #         request.session['dept'] = m.staff.dept.id
        #         request.session['uname'] = m.staff.email
        #         # request.session['fname'] = e.first_name
        #         # request.session['lname'] = e.last_name
        #         # request.session['eid'] = e.id
        #         # request.session['image'] = str(e.profile_image)
        #         return redirect('index')

    return render(request, 'employee/login.html', {})


def profile(request):
    fname = request.session.get('user')
    st = staff.objects.filter(id=fname)
    return render(request, 'employee/profile.html', {'emp': st})


# def projects(request):
#     project_list = project.objects.all()
#     eid = request.session.get('eid')
#     p1 = ''
#     for p in project_list:
#         if p.emp_id == eid:
#             p1 = project.objects.filter(emp_id=eid)
#     context_dict = {'projects': p1}
#     return render(request, 'employee/project_list.html', context_dict)


def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect('index')


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

    return render(request, 'employee/leave_request.html', {'dname': st.dept, 'ename': st.first_name, 'dept_id': st.dept_id, 'emp_id': st.id, 'emp_leave': emp_leave, 'msg': msg})


# def about_us(request):
#     return render(request, 'employee/about-us.html', {})


def edit(request, eid):
    emp = employee.objects.filter(id=eid)
    s = staff.objects.filter(id=eid)
    if request.method == 'POST':
        s = staff.objecys.get(id=eid)
        s.first_name=request.POST.get('fname'),
        print(s.first_name)
        s.email=request.POST.get('email'),
        s.last_name=request.POST.get('lname'),
        s.gender=request.POST.get('gender'),
        s.date_of_birth=request.POST.get('dob'),
        s.password=request.POST.get('password'),
        s.phone_no=request.POST.get('phone_no'),
        s.address=request.POST.get('address'),
        s.city=request.POST.get('city'),
        s.qualification=request.POST.get('qualification'),
        s.designation=request.POST.get('designation'),
        s.skills=request.POST.get('skills'),
        s.experience=request.POST.get('experience'),
        s.date_of_joining=request.POST.get('doj'),
        s.salary=request.POST.get('salary'),
        s.profile_image=request.FILES.get(
            'profile_image')

        s.save()
        e = employee.objects.create(staff=s)
        e.save()
        # e = employee.objects.get(id=eid)
        # e.first_name = request.POST.get('fname')
        # e.last_name = request.POST.get('lname')
        # e.phone_no = request.POST.get('phone_no')
        # e.address = request.POST.get('address')
        # e.city = request.POST.get('city')
        # e.designation = request.POST.get('designation')
        # e.skills = request.POST.get('skills')
        # e.experience = request.POST.get('experience')
        # if request.FILES.get('profile_image'):
        #     e.profile_image = request.FILES.get('profile_image')

        # e.salary = request.POST.get('salary')
        # e.save()
        # return redirect('employees_list')
    return render(request, 'employee/edit.html', {'emp': emp})


# def delete_employee(request, eid):
#     e = employee.objects.get(id=eid)
#     e.delete()
#     return redirect('employees_list')


def show_leaves(request):
    eid = request.session.get('user')
    print(eid)
    leaves = leave.objects.filter(staff=eid)
    context_dict = {'leaves': leaves}
    return render(request, 'employee/show_leaves.html', context_dict)


# def approve(request, lid):
#     # l = leave.objects.filter(id=lid)
#     if request.method == "POST":
#         le = leave.objects.get(id=lid)
#         le.leave_status = 'Approve'
#         le.save()
#         return redirect('show_leaves')
#     return render(request, 'employee/show_leaves.html')


# def deny(request, lid):
#     l = leave.objects.filter(id=lid)
#     if request.method == "POST":
#         le = leave.objects.get(id=lid)
#         le.leave_status = 'Deny'
#         le.save()
#         return redirect('show_leaves')
#     return render(request, 'employee/show_leaves.html')


# def all_projects(request):
#     if request.method == 'POST':
#         name = request.POST.get('search')
#         project_list = project.objects.filter(project_name__istartswith=name)
#         context_dict = {'projects': project_list}
#     else:
#         project_list = project.objects.all()
#         context_dict = {'projects': project_list}
#     return render(request, 'employee/all_projects.html', context_dict)


# def fill_by_dept(request):
#     dept = department.objects.all()
#     dept_id = request.GET.get('dept_id')

#     emp = employee.objects.filter(dept=dept_id)
#     for e in emp:
#         print(e.first_name)
#     return render(request,'employee/add_project.html',{'dept':dept,'emp':emp})


def employee_register(request):
    dept = department.objects.all()
    if request.method == 'POST':
        
        # s = staff()
        # e = employee()
        # a = department.objects.get(dept_name = request.POST.get('dept'))
        # s.dept = a
        # s.first_name = request.POST.get('fname')
        # s.last_name = request.POST.get('lname')
        # s.gender = request.POST.get('gender')
        # s.date_of_birth = request.POST.get('dob')
        # s.email = request.POST.get('email')
        # s.password = request.POST.get('password')
        # s.phone_no = request.POST.get('phone_no')
        # s.address = request.POST.get('address')
        # s.city = request.POST.get('city')
        # s.qualification = request.POST.get('qualification')
        # s.designation = request.POST.get('designation')
        # s.skills = request.POST.get('skills')
        # s.experience = request.POST.get('experience')
        # s.date_of_joining = request.POST.get('doj')
        # if request.FILES.get('profile_image'):
        #     s.profile_image = request.FILES.get('profile_image')

        # s.salary = request.POST.get('salary')
        # e.save(s)

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
        # e.save(s)
#         subject = 'Employee Management System'
#         message = 'Username:  '+e.email + '\nPassword: '+ e.password
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [e.email,]
#         send_mail(subject,message,email_from,recipient_list)
        return redirect('employees_list')
    return render(request, 'employee/employee_register.html', {'dept': dept})


def manager_list(request):
    manage = manager.objects.all()
    return render(request, 'employee/manager_list.html', {'employees': manage})

#  def help_desk(request):
#     return render(request,'employee/help_desk.html', {})

# def demo(request):
#     return render(request,'employee/demo.html', {})


# def complete(request, pid):
#     if request.method == "POST":
#         pr = project.objects.get(id=pid)
#         print(pid)
#         pr.project_status = 'complete'
#         pr.save()
#         return redirect('all_projects')
#     return render(request, 'employee/all_projects.html')

# def search(request):
#     error = False
#     if 'search' in request.GET:
#         q = request.GET['search']
#         if not q:
#             error = True
#         elif len(q) > 20:
#             error = True
#         else:
#             emp = employee.objects.filter(first_name=q)
#             return render(request, 'employee/employee_list.html', {'emp':emp, 'query': q})
#     return render(request, 'employee/employee_list.html', {'error': error})
