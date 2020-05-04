from django.db import models
from datetime import datetime
import re, bcrypt

class physicianManager(models.Manager):

    def register_validator(self,postData):
        errors = {}
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First name must be filled out and at least 2 characters long!"
        if len(postData['l_name']) < 2:
            errors['l_name'] = "Last name must be filled out and at least 2 characters long!"

        # Checks email format (make sure to import re)
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Invalid email address!"

        # Registration Code Validation
        if postData['code'] != '1111':
            errors['code'] = "Registration Code is Incorrect!"

        # looks to see if email is already in database
        elif len(Physician.objects.filter(email=postData['email'])) > 0:
            errors['existingEmail'] = "Email is already taken by another Physician"
        
        # Checks length of password, and if long enough, will check the passwords against eachother
        if len(postData['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters!"
        elif postData['pw'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Password does not match confirm password field!"

        return errors

    def login_validator(self,postData):
        errors = {}
        # Checks to see if email matches record in db
        phys = Physician.objects.filter(email=postData['email'])
        if len(phys) < 1:
            errors['emailDoesNotExist'] = "Email does not exist"

        # if email exists, checks inputted password (bcypt hashed) against the record's hashed pw
        else:
            logged_phys = phys[0]
            if not bcrypt.checkpw(postData['pw'].encode(), logged_phys.password.encode()):
                errors['badPW'] = "Password is incorrect!!"

        return errors

class Physician(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = physicianManager()

class patientManager(models.Manager):

    def register_validator(self,postData):
        errors = {}
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First name must be filled out and at least 2 characters long!"
        if len(postData['l_name']) < 2:
            errors['l_name'] = "Last name must be filled out and at least 2 characters long!"

        # Checks email format (make sure to import re)
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Invalid email address!"
        
        if len(postData['phys']) <1:
            errors['phys'] = "You must select a physician!"

        # DOB validation
        if postData['dob'] == '':
            errors['dob_empty'] = "Date of Birth must be filled out!"
        elif datetime.strptime(postData['dob'], "%Y-%m-%d") > datetime.now():
            errors['dob'] = "Date of birth must be in the past!"

        # looks to see if email is already in database
        elif len(Patient.objects.filter(email=postData['email'])) > 0:
            errors['existingEmail'] = "Email is already taken by another user"
        
        # Checks length of password, and if long enough, will check the passwords against eachother
        if len(postData['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters!"
        elif postData['pw'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Password does not match confirm password field!"

        return errors

    def login_validator(self,postData):
        errors = {}
        # Checks to see if email matches record in db
        pt = Patient.objects.filter(email=postData['email'])
        if len(pt) < 1:
            errors['emailDoesNotExist'] = "Email does not exist"

        # if email exists, checks inputted password (bcypt hashed) against the record's hashed pw
        else:
            logged_pt = pt[0]
            if not bcrypt.checkpw(postData['pw'].encode(), logged_pt.password.encode()):
                errors['badPW'] = "Password is incorrect!!"

        return errors

class Patient(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    dob = models.DateField()
    phys = models.ForeignKey(Physician, related_name="patients", on_delete = models.CASCADE)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = patientManager()

class taskManager(models.Manager):

    def task_validator(self,postData):
        errors = {}
        if not 'pt' in postData:
            errors['pt'] = "You must select a patient!"
        if 'taskSelect' in postData:
            if len(postData['taskInput']) > 0:
                errors['duplicateTask'] = "Please either SELECT or INPUT a task, but NOT both!"
        elif len(postData['taskInput']) < 1:
            errors['task'] = "Task Item is required!"
        if len(postData['desc']) < 1:
            errors['desc'] = "Task description is required!"
        if len(postData['date']) < 1:
            errors['dateEmpty'] = "Due Date is required!"
        # elif datetime.strptime(postData['date'], "%Y-%m-%d" ) < datetime.now():
        #     errors['datePast'] = "Due Date must be in the future!"

        return errors

class Task(models.Model):
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default = "Upcoming")
    desc = models.TextField()
    date = models.DateField()
    pt = models.ForeignKey(Patient, related_name="tasks", on_delete = models.CASCADE)
    phys = models.ForeignKey(Physician, related_name="tasks", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = taskManager()