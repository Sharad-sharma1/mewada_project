from django.db import models


Gender = [
          ('', ''), 
          ('Male', 'Male'), 
          ('Female', 'Female'), 
          ('Other', 'Other')
]

choice = [
          ('Yes', 'Yes'), 
          ('No', 'No')
]

# Create your models here.
class Village(models.Model):
  village_name = models.CharField(max_length=50)
  usr_in_village = models.CharField(max_length=10, default=0)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

  class Meta:
        ordering = ('village_name',)

  def __str__(self):
      return self.village_name

class Area(models.Model):
  area_name = models.CharField(max_length=50)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

  class Meta:
        ordering = ('area_name',)

  def __str__(self):
      return self.area_name

class Main_User_Table(models.Model):
  usercode =  models.CharField(max_length=40, blank=True)
  name  =  models.CharField(max_length=50)
  father_or_husband_name  =  models.CharField(max_length=50, blank=True)
  surname  =  models.CharField(max_length=50)
  mother_name  =  models.CharField(max_length=50, blank=True)
  gender  =  models.CharField(max_length=6, blank=True,choices=Gender)
  birth_date  =  models.DateField(default='1901-01-01')
  mobile_no1  =  models.CharField(max_length=15, blank=True)
  mobile_no2  =  models.CharField(max_length=15, blank=True)
  area = models.ForeignKey(Area, on_delete=models.PROTECT, default=None) 
  village = models.ForeignKey(Village, on_delete=models.PROTECT, default=None)
  address  =  models.CharField(max_length=100, blank=True)
  pincode =  models.CharField(max_length=10, blank=True)
  occupation = models.CharField(max_length=20, blank=True)
  country = models.CharField(max_length=15, default='India', blank=True)
  state = models.CharField(max_length=15, default='Gujarat', blank=True)
  email_id = models.CharField(max_length=100, blank=True)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  active_flag = models.CharField(max_length=10, default='Active',choices=[('Sifted', 'Sifted'), ('Deleted', 'Deleted')])
  delete_flag = models.CharField(max_length=6, blank=True,choices=choice)
  death_flag = models.CharField(max_length=6, blank=True,choices=choice)
  receipt_flag = models.CharField(max_length=6, blank=True,choices=choice)
  receipt_no = models.CharField(max_length=20, blank=True)
  receipt_date = models.DateField(default='2001-11-1')
  receipt_amt = models.CharField(max_length=20, blank=True)

  def __str__(self):
    return '%s %s %s %s' %(self.name, self.father_or_husband_name, self.area, self.village)

class Premium_User_Table(models.Model):
  name  =  models.CharField(max_length=50)
  father_or_husband_name  =  models.CharField(max_length=50, blank=True)
  surname  =  models.CharField(max_length=50)
  birth_date  =  models.DateField(default='1901-01-01')
  mobile_no1  =  models.CharField(max_length=15, blank=True)
  mobile_no2  =  models.CharField(max_length=15, blank=True)
  area = models.ForeignKey(Area, on_delete=models.PROTECT, default=None) 
  village = models.ForeignKey(Village, on_delete=models.PROTECT, default=None)
  address  =  models.CharField(max_length=100, blank=True)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  active_flag = models.CharField(max_length=10, default='Active',choices=[('Sifted', 'Sifted'), ('Deleted', 'Deleted')])
  delete_flag = models.CharField(max_length=6, blank=True,choices=choice)
  death_flag = models.CharField(max_length=6, blank=True,choices=choice)
  receipt_no = models.CharField(max_length=20, blank=True)
  receipt_date = models.DateField(default='2001-11-1', null=True, blank=True)

  def __str__(self):
    return '%s %s %s %s' %(self.name, self.father_or_husband_name, self.area, self.village)