from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from employee import views
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('departments/', views.departments, name='department_list'),
    path('employees/', views.employees, name='employees_list'),
    path('manager_list/', views.manager_list, name='manager_list'),
    path('edit/<eid>', views.edit_employee, name='edit_employee'),
    path('delete/<eid>', views.delete_employee, name='delete_employee'),
    path('emp_assign_projects/', views.projects, name='projects'),
    path('profile/', views.profile, name='profile'),
    path('leave_request/', views.leave_request, name='leave_request'),
    path('show_leaves/', views.show_leaves, name='show_leaves'),
    
    path('approve/<lid>', views.approve, name='approve'),
    path('deny/<lid>', views.deny, name='deny'),
    path('all_project/', views.all_projects, name='all_projects'),
    path('add_project/', views.add_project, name='add_project'),
    path('filter_by_dept/', views.filter_by_dept, name='filter_by_dept'),
    path('employee_register/', views.employee_register, name='employee_register'),
    path('complete/<pid>', views.complete, name='complete'),    
    path('updates/', views.updates, name='updates'),    
    path('time_sheet/', views.timesheet, name='time_sheet'),      
    path('assign_project/<uid>', views.assign_project, name='assign_project'),    
    path('abc/', views.abc, name='abc'),    
    path('holiday/', views.holiday, name='holiday'),
    path('leave_format/', views.leave_format, name='leave_format'),
    path('update_mail/', views.update_mail, name='update_mail'),
    path('policy/', views.policy,name='policy'),
    path('help_desk/', views.help_desk, name='help_desk'),
    path('change_password/', views.change_password, name='change_password'),
    path('base1/', views.base1, name='base1'),
    path('project_info/', views.project_info, name='project_info'),  
    path('project_inquiry/', views.project_inquiry1, name='project_inquiry'),
    path('check_query/<pid>', views.check_inquiry, name='check_query'),
    path('project_complete/<pid>', views.project_complete, name='project_complete'),
    path('project_inprogress/<pid>', views.project_inprogress, name='project_inprogress'),
    path('reply/<pid>', views.reply, name='reply'),
    path('edit_project/<pid>', views.edit_project, name='edit_project'),
    path('delete_project/<pid>', views.delete_project, name='delete_project'),
    # path('date/', views.datepick, name='date'),
    # path('demo/', views.demo, name='demo'),
    path('leave_report/', views.report, name='leave_report'),
    path('range/', views.range, name='range'),
    # path('emp_assign/<eid>', views.emp_assign, name='emp'),
     path('inquiry1/', views.inquiry1, name='inquiry1'),
  
   
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
