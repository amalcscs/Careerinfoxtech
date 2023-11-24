from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class department(models.Model):
     name = models.CharField(max_length=100)
     description = models.CharField(max_length=100)
  
class candidates (models.Model):
    fullname =  models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password  = models.CharField(max_length=100)
    username  = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    reference = models.CharField(null=True,blank=True,max_length=100)
    college = models.CharField(null=True,blank=True,max_length=200,default='')
    qualifications = models.CharField(null=True,blank=True,max_length=100)
    passout_year = models.IntegerField(null=True,blank=True,default='')
    exam_status = models.CharField(max_length=20,default='0')
    mark = models.IntegerField(default='0')
    regdate=models.DateField(default='')
    contact_status=models.CharField(max_length=20,default='0')
    replay_status=models.CharField(max_length=20,default='0')
    deptmnt = models.ForeignKey(department, on_delete=models.SET_NULL,related_name='dep', null=True, blank=True, default='')
    te_status = models.CharField(max_length=20,default='0')
   
class designation(models.Model):
     designation = models.CharField(max_length=100)

class catagory(models.Model):
    name = models.CharField(max_length=100) 
    no_of_question = models.CharField(max_length=100)
    time_taken = models.IntegerField()
                                                                    
class question(models.Model):
    questions = models.CharField(max_length=200)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)    
    correct_option = models.CharField(max_length=100)
    ctgry_id = models.CharField(max_length=100,default='')
    dept_id = models.CharField(max_length=100,default='')

class login(models.Model):
    designation = models.ForeignKey(designation, on_delete=models.SET_NULL, related_name='desgn',null=True,blank=True, default='')
    fullname = models.CharField(max_length=200)
    email=models.EmailField(max_length=200,default='')
    contact_no=models.CharField(max_length=200,default='')
    password = models.CharField(max_length=100)
    image = models.FileField(upload_to= 'images/')

class adminlimit(models.Model):
    no_of_question = models.IntegerField()
    time_taken = models.IntegerField()

class time_out(models.Model):
    category = models.ForeignKey(catagory,on_delete=models.SET_NULL,null=True,blank=True,related_name="category",default='')
    user = models.ForeignKey(candidates,related_name="user",on_delete=models.SET_NULL,null=True,blank=True,default='')
    exam_status = models.CharField(max_length=100,default='0')
    
    
    
class exam_timing(models.Model):
    from_date_time = models.DateTimeField()
    to_date_time = models.DateTimeField()