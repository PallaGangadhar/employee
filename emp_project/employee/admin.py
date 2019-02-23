from django.contrib import admin
from employee.models import department, staff, leave, project, employee, manager
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail
from django.conf import settings


class manager_list(admin.ModelAdmin):
    list_display = ('staff_id','staff')

class employee_list(admin.ModelAdmin):
    list_display = ('id','staff_id','staff')

    
#     def save_model(self,request,obj,form,change):
#         subject = 'Employee Management System'
#         message = 'Username:  '+obj.email + '\nPassword: '+ obj.password
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [obj.email,]
#         send_mail(subject,message,email_from,recipient_list)
#         super().save_model(request, obj, form, change)
        
# class project_list(admin.ModelAdmin):
#     list_display = ('project_name','emp','dept','project_technology','project_start_date','project_end_date','project_status')
#     def save_model(self,request,obj,form,change):
#         subject = 'Employee Management System'
#         message = 'You have been assigned a new project' + '\nProject Name: ' + obj.project_name
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [obj.emp.email,]
#         send_mail(subject,message,email_from,recipient_list)
#         super().save_model(request, obj,form,change)
   
    # change_list_template = "admin/models_change_list.html"

class leave_request(admin.ModelAdmin):
    list_display = ('dept', 'staff', 'leave_reason', 'leave_time', 'leave_date')
    change_list_template = "admin/manage_list.html"
    

admin.site.register(department)
admin.site.register(staff)
admin.site.register(employee, employee_list)
admin.site.register(manager, manager_list)
# admin.site.register(salary)
admin.site.register(leave, leave_request)
admin.site.register(project)
admin.site.unregister(Group)

admin.site.site_header = ("Employee Management System")
admin.site.site_title = ("EMS")
admin.site.index_title = ("Administraion")