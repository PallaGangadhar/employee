from django.contrib import admin
from employee.models import department, staff, leave, project, employee, manager,project_assingment,time_sheet,project_inquiry
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Q,Subquery


class manager_list(admin.ModelAdmin):
    list_display = ('first_name','last_name','doj','email','phone_no','city','qualification','designation','skills','experience','image')
    
    def first_name(self, instance):
        return instance.staff.first_name
    def last_name(self, instance):
        return instance.staff.last_name
    def doj(self, instance):
        return instance.staff.date_of_joining
    def email(self, instance):
        return instance.staff.email
    def phone_no(self, instance):
        return instance.staff.phone_no
    def city(self, instance):
        return instance.staff.city
    def qualification(self, instance):
        return instance.staff.qualification
    def designation(self, instance):
        return instance.staff.designation
    def skills(self, instance):
        return instance.staff.skills
    def experience(self, instance):
        return instance.staff.experience                       
    def image(self,instance):
        return mark_safe('<img src="/media/%s" width="50" height="50"  />' % (instance.staff.profile_image))
    
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Manager Details'}
        return super(manager_list, self).changelist_view(request, extra_context=extra_context)
    list_per_page = 5
    
class employee_list(admin.ModelAdmin):
    list_display = ('first_name','last_name','doj','email','phone_no','city','qualification','designation','skills','experience','image')
    def first_name(self, instance):
        return instance.staff.first_name
    def last_name(self, instance):
        return instance.staff.last_name
    def doj(self, instance):
        return instance.staff.date_of_joining
    def email(self, instance):
        return instance.staff.email
    def phone_no(self, instance):
        return instance.staff.phone_no
    def city(self, instance):
        return instance.staff.city
    def qualification(self, instance):
        return instance.staff.qualification
    def designation(self, instance):
        return instance.staff.designation
    def skills(self, instance):
        return instance.staff.skills
    def experience(self, instance):
        return instance.staff.experience                       
    def image(self,instance):
        return mark_safe('<img src="/media/%s" width="50" height="50"/>' % (instance.staff.profile_image))
    change_list_template = "admin/leave.html"
    list_per_page = 5
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    actions = None
    list_display_links = None
    
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Employee Details'}
        
        return super(employee_list, self).changelist_view(request, extra_context=extra_context)

        
class project_list(admin.ModelAdmin):
    list_display = ('project_name','project_technology','start_date','end_date','project_status')
    # def save_model(self,request,obj,form,change):
    #     subject = 'Employee Management System'
    #     message = 'You have been assigned a new project' + '\nProject Name: ' + obj.project_name
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = [obj.emp.email,]
    #     send_mail(subject,message,email_from,recipient_list)
    #     super().save_model(request, obj,form,change)
   
    change_list_template = "admin/leave.html"
    list_display_links = None
    list_per_page = 5
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    actions = None
    
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Project Details'}
        return super(project_list, self).changelist_view(request, extra_context=extra_context)
    def start_date(self, obj):
        return obj.project_start_date.strftime("%Y-%m-%d")
    def end_date(self, obj):
        return obj.project_end_date.strftime("%Y-%m-%d")

class leave_request(admin.ModelAdmin):
    list_display = ('dept','staff', 'leave_reason', 'leave_time', 'leave_date','leave_status')
    change_list_template = "admin/manage_list.html"
    # list_per_page = 5
    list_display_links = None
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('mleave/', self.my_view,name='mleave'),
            path('eleave/', self.my_view1,name='eleave'),
            path('eleave/', self.my_view1,name='eleave'),
            path('manager_approve/<lid>', self.manager_approve,name='manager_approve'),
            path('manager_deny/<lid>', self.manager_deny,name='manager_deny'),
        ]
        return my_urls + urls

    def my_view(self,request):
        superusers = User.objects.filter(is_superuser=True)
        m = leave.objects.filter(staff__id__in=Subquery(manager.objects.all().values('staff'))).order_by('-id')
        data = {'test': 'test',
        'opts': self.model._meta,    
        'change': True,
        'is_popup': False,
        'save_as': False,
        'has_delete_permission': False,
        'has_add_permission': False,
        'has_change_permission': False,
        'm':m,
        'super':superusers}
        return TemplateResponse(request,'admin/mleave.html',data)

    def my_view1(self,request):
        m = leave.objects.filter(staff__id__in=Subquery(employee.objects.all().values('staff')))
        data = {'test': 'test',
        'opts': self.model._meta,    
        'change': True,
        'is_popup': False,
        'save_as': False,
        'has_delete_permission': False,
        'has_add_permission': False,
        'has_change_permission': False,
        'm':m}
        
        return TemplateResponse(request,'admin/eleave.html',data)

    def manager_approve(self,request, lid):
        if request.method == "POST":
            le = leave.objects.get(id=lid)
            le.leave_status = 'Approve'
            le.save()
            return redirect('admin/mleave.html')
        
    def manager_deny(self,request, lid):
        if request.method == "POST":
            le = leave.objects.get(id=lid)
            le.leave_status = 'Deny'
            le.save()
        return redirect('admin/mleave.html')
    
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Staff Leave Details'}
        return super(leave_request, self).changelist_view(request, extra_context=extra_context)
   

class assign_projects(admin.ModelAdmin):
    list_display = ('emp','project','dept_name','status')  
    change_list_template = "admin/leave.html"
    def dept_name(self, instance):
        return instance.emp.staff.dept.dept_name

    def assign_projects(self, request, extra_context=None):
        extra_context = {'title': 'Project Assignment Details'}
        return super(assign_projects, self).changelist_view(request, extra_context=extra_context)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False
    # actions = None
    # list_display_links = None
    # list_per_page = 5
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Assign Project Details'}
        return super(assign_projects, self).changelist_view(request, extra_context=extra_context)
    
class timesheet_details(admin.ModelAdmin):
    list_display = ('project','staff','date','time','description')
    def project(self, instance):
        return instance.pid.project_name
    def staff(self, instance):
        return instance.staff.first_name
    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False
    list_per_page = 5
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'TimeSheet Details'}
        return super(timesheet_details, self).changelist_view(request, extra_context=extra_context)
    actions = None
    # list_display_links = None
    change_list_template = "admin/leave.html"   

class staff_view(admin.ModelAdmin):
    list_per_page = 5

class inquiry(admin.ModelAdmin):
    list_display = ('staff','project','comment','reply')
    list_per_page = 5

admin.site.register(department)
admin.site.register(project_inquiry,inquiry)
admin.site.register(staff,staff_view)
admin.site.register(project_assingment,assign_projects)
admin.site.register(time_sheet,timesheet_details)
admin.site.register(employee, employee_list)
admin.site.register(manager, manager_list)
admin.site.register(leave, leave_request)
admin.site.register(project, project_list)
admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.site_header = ("Employee Management System")
admin.site.site_title = ("EMS")
admin.site.index_title = ("Admin Panel")

