from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
# Create your models here.
from django.core.exceptions import ValidationError
USER_TYPE_CHOICES = (
    ('Employee', 'Employee'),
    ('Manager', 'Manager'),
)


class department(models.Model):
    dept_name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Department'

    def __str__(self):
        return self.dept_name


class staff(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    dept = models.ForeignKey(department, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, blank=False, default='')
    last_name = models.CharField(max_length=128, blank=False, default='')
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=128)
    date_of_joining = models.DateField(blank=True, null=True)
    email = models.EmailField(
        max_length=128, blank=False, unique=True, default='')
    password = models.CharField(
        max_length=50, blank=False, default='')
    phone_no = models.CharField(max_length=128, unique=True)
    address = models.CharField(max_length=128, blank=False)
    city = models.CharField(max_length=128, blank=False)
    qualification = models.CharField(max_length=128, blank=False)
    designation = models.CharField(max_length=128, blank=False)
    skills = models.CharField(max_length=128, blank=False)
    experience = models.IntegerField(blank=False)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
    salary = models.IntegerField(default=0)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="120" height="120" />' % (self.profile_image))

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name_plural = 'Staff'

class employee(models.Model):
    staff = models.ForeignKey(staff, on_delete=models.CASCADE)
    def __str__(self):
        return self.staff.first_name
    class Meta:
        verbose_name_plural = 'Employee'

class manager(models.Model):
    staff = models.ForeignKey(staff, on_delete=models.CASCADE)
   

    class Meta:
        verbose_name_plural = 'Manager'

class leave(models.Model):
    dept = models.ForeignKey(department, on_delete=models.CASCADE)
    staff = models.ForeignKey(staff, on_delete=models.CASCADE)
    leave_reason = models.CharField(max_length=128, blank=False)
    leave_date = models.DateField(default=0, blank=True)
    leave_time = models.CharField(max_length=128, default=0)
    leave_status = models.CharField(max_length=128, default='',blank=True)

    class Meta:
        verbose_name_plural = 'Leave'

    def __str__(self):
        return self.leave_reason


class project(models.Model):
    status = (('complete', 'Complete'),
              ('incomplete', 'Incomplete'))
    dept = models.ForeignKey(department, on_delete=models.CASCADE,default='')
    project_name = models.CharField(max_length=128, blank=False)
    project_start_date = models.DateField(blank=False)
    project_end_date = models.DateField(blank=False)
    project_technology = models.CharField(max_length=128, blank=False)
    project_status = models.CharField(max_length=128, blank=False, choices=status, default="incomplete")

    class Meta:
        verbose_name_plural = 'Project'

    def __str__(self):
        return self.project_name

    # def clean(self):
    #     """ warn if selected city is not in selected country """
    #     if (self.dept and self.staff and self.staff.dept.id != self.dept.id):
    #         raise ValidationError(message='%(emp_name)s is not in %(dept_name)s',
    #                               code='wrong_country',
    #                               params=dict(emp_name=self.staff.first_name,
    #                                           dept_name=self.dept.dept_name))

class time_sheet(models.Model):
    pid = models.ForeignKey(project, on_delete=models.Model)
    staff = models.ForeignKey(staff, on_delete=models.Model)
    date = models.DateField(blank=False)
    time = models.IntegerField(blank=False)
    description = models.CharField(max_length=128, blank=False)

    class Meta:
        verbose_name_plural = 'Time Sheet'

    def __str__(self):
        return self.pid.project_name

class project_assingment(models.Model):
    status = (('complete', 'Complete'),
            ('inprogress', 'Inprogress'),
            ('incomplete','Incomplete'))
    emp = models.ForeignKey(employee, on_delete=models.CASCADE,default='')
    project = models.ForeignKey(project, on_delete=models.CASCADE, default='')
    status = models.CharField(max_length=128, blank=False, choices=status, default="incomplete")


    class Meta:
        verbose_name_plural = 'Assigned Projects'

    def __str__(self):
        return self.project.project_name

class project_inquiry(models.Model):
    staff = models.ForeignKey(staff, on_delete=models.CASCADE)
    project = models.ForeignKey(project_assingment, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.CharField(max_length=128, blank=False)
    time = models.CharField(max_length=128,blank=False)
    reply = models.CharField(max_length=128,blank=True,default='no')

    class Meta:
        verbose_name_plural = 'Project Inquiry'

    def __str__(self):
        return self.project.project.project_name

