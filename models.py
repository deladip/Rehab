from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Emp(models.Model):
    DISCIPLINE = (
            ('PT', 'PT'),
            ('OT', 'OT'),
            ('SLP','SLP'),
            ('PTA','PTA'),
            ('COTA','COTA'),
            )

    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE)       
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null= True)
    profile_pic = models.ImageField(default="usericon.png",null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    userLicense = models.CharField(max_length=11, null=True)
    discpline = models.CharField(max_length=20,null=True, choices=DISCIPLINE)
    npi = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class PatientList(models.Model):

    CLINICAL_SETTING =(
        ('workers_Comp', 'WC'),
        ('homeHealth', 'HH'),
        ('medicareB', 'MB'),
         )

    REFER=(
        ('PT', 'PT Eval'),
        ('OT', 'OT Eval'),
        ('SLP', 'SLP Eval'),
         )

    FACILITY=(
        ('Assisted', 'ALF'),
        ('Independent', 'IND'),
        ('AdultDay', 'ADC'),
        ('Home', 'HOME'),
         )

    
    name = models.CharField(max_length=200, null=True)
    zipCode = models.CharField(max_length=5, null=True)
    refer = models.CharField(max_length=20, null=True, choices=REFER)
    setting = models.CharField(max_length=20, null=True,choices=CLINICAL_SETTING)
    facility = models.CharField(max_length=20, null=True,choices=FACILITY)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Eval', 'Eval'),
        ('Follow up', 'Follow up'),
        ('Discharge', 'Discharge'),
    )

    emp = models.ForeignKey(Emp, null=True, on_delete=models.SET_NULL)
    patient = models.ForeignKey(PatientList, null=True, on_delete=models.SET_NULL)
    date_created = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=True, choices=STATUS)
    note = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.patient.name

class Appointment(models.Model):
         first_name = models.CharField(max_length=20, null=True)
         last_name = models.CharField(max_length=20, null=True)
         phone = models.CharField(max_length=50)
         dob = models.DateTimeField(auto_now_add=True)
         p_insurance = models.CharField(max_length=20, null=True)
         s_insurance = models.CharField(max_length=20, null=True)
         address = models.CharField(max_length=1000, null=True)
         date_created = models.DateField(auto_now_add=True)
         appointment_day = models.DateTimeField(auto_now_add=True)


    
    