from django.contrib import admin
from employee.models import department, staff, leave, project, employee, manager,project_assingment,time_sheet,project_inquiry
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
  
    
#     def save_model(self,request,obj,form,change):
#         subject = 'Employee Management System'
#         message = 'Username:  '+obj.email + '\nPassword: '+ obj.password
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [obj.email,]
#         send_mail(subject,message,email_from,recipient_list)
#         super().save_model(request, obj, form, change)
        
class project_list(admin.ModelAdmin):
    list_display = ('id','project_name','project_technology','project_start_date','project_end_date','project_status')
    # def save_model(self,request,obj,form,change):
    #     subject = 'Employee Management System'
    #     message = 'You have been assigned a new project' + '\nProject Name: ' + obj.project_name
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = [obj.emp.email,]
    #     send_mail(subject,message,email_from,recipient_list)
    #     super().save_model(request, obj,form,change)
   
    # change_list_template = "admin/leave.html"
    # list_display_links = None
    # list_per_page = 5
    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False
    # actions = None

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Project Details'}
        return super(project_list, self).changelist_view(request, extra_context=extra_context)

class leave_request(admin.ModelAdmin):
    list_display = ('dept','staff', 'leave_reason', 'leave_time', 'leave_date','leave_status')
    change_list_template = "admin/leave.html"
    list_per_page = 5

class assign_projects(admin.ModelAdmin):
    list_display = ('emp','project','dept_name','status')  
    # change_list_template = "admin/leave.html"
    def dept_name(self, instance):
        return instance.emp.staff.dept.dept_name

    # def assign_projects(self, request, extra_context=None):
    #     extra_context = {'title': 'Project Assignment Details'}
    #     return super(assign_projects, self).changelist_view(request, extra_context=extra_context)

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
    list_display = ('project','staff','date','time')
    def project(self, instance):
        return instance.pid.project_name
    def staff(self, instance):
        return instance.staff.first_name
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    list_per_page = 5
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Project Details'}
        return super(timesheet_details, self).changelist_view(request, extra_context=extra_context)
    actions = None
    list_display_links = None
    change_list_template = "admin/leave.html"   

class staff_view(admin.ModelAdmin):
    list_per_page = 5

admin.site.register(department)
admin.site.register(staff,staff_view)
admin.site.register(project_assingment,assign_projects)
admin.site.register(time_sheet,timesheet_details)
admin.site.register(employee, employee_list)
admin.site.register(manager, manager_list)
# admin.site.register(salary)
admin.site.register(leave, leave_request)
admin.site.register(project, project_list)
admin.site.register(project_inquiry)
admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.site_header = ("Employee Management System")
admin.site.site_title = ("EMS")
admin.site.index_title = ("Admin Panel")

