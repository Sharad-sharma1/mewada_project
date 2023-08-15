from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from . models import *

class Login_Form(AuthenticationForm, forms.ModelForm):
    username = forms.CharField(label_suffix='', widget=forms.TextInput(attrs={'class':'form-control', 'id':'usr_name'}))
    password = forms.CharField(label_suffix='', widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'pwd'})) 
    class Meta:
        model = User
        fields = ['username', 'password']

class Village_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Village
        fields = ['village_name']
        widgets = {
            'village_name':forms.TextInput(attrs={'class':'form-control'}),
            'village_code':forms.TextInput(attrs={'class':'form-control'}),
        }
        
class Area_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Area
        fields = '__all__'
        widgets = {
            'area_name':forms.TextInput(attrs={'class':'form-control'}),
        }
    
class DateInput(forms.DateInput):
    input_type = 'date'

class Add_User_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Main_User_Table
        fields = ['name','father_or_husband_name','surname','gender','mobile_no1','mobile_no2','birth_date',
                    'address','pincode','area','village','country','state']
        labels = { 
            'usercode': 'User Code',
            'name':'Name *',
            'father_or_husband_name':'Father/Middle Name',
            'surname':'Surname *',
            'mother_name':'Mother Name',
            'gender':'Gender',
            'birth_date':'Birth Date',
            'mobile_no1':'Mobile Number',
            'mobile_no2':'Mobile Number 2',
            'address':'Address',
            'area':'Area *',
            'village':'Village *',
            'pincode':'Pincode',
            'occupation':'Occupation',
            'country':'Country',
            'state':'State',
            'email_id':'Email ID'
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'father_or_husband_name':forms.TextInput(attrs={'class':'form-control'}),
            'surname':forms.TextInput(attrs={'class':'form-control'}),
            'mother_name':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(choices=Gender,attrs={'class':'form-control form-select'}),
            'birth_date':DateInput(attrs={'class':'form-control'}),
            'mobile_no1':forms.TextInput(attrs={'class':'form-control'}),
            'mobile_no2':forms.TextInput(attrs={'class':'form-control'}),
            'area':forms.Select(attrs={'class':'form-control form-select'}),
            'village':forms.Select(attrs={'class':'form-control form-select'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'pincode':forms.TextInput(attrs={'class':'form-control'}),
            'occupation':forms.TextInput(attrs={'class':'form-control'}),
            'country':forms.TextInput(attrs={'class':'form-control','disabled': True}),
            'state':forms.TextInput(attrs={'class':'form-control','disabled': True}),
            'email_id':forms.TextInput(attrs={'class':'form-control'}),
        }


class Update_User_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Main_User_Table

        ordering = ['id']
        
        fields = [
            'name','father_or_husband_name','mother_name','surname','birth_date', 'gender','mobile_no1',
            'mobile_no2','email_id','active_flag','address','pincode','area','village','country','state','receipt_date'
        ]
        labels = { 
            'usercode': 'User Code',
            'name':'Name *',
            'father_or_husband_name':'Father/Middle Name',
            'surname':'Surname *',
            'mother_name':'Mother Name',
            'gender':'Gender',
            'birth_date':'Birth Date',
            'mobile_no1':'Mobile Number',
            'mobile_no2':'Mobile Number 2',
            'address':'Address',
            'area':'Area *',
            'village':'Village *',
            'pincode':'Pincode',
            'occupation':'Occupation',
            'country':'Country',
            'state':'State',
            'email_id':'Email ID',
            'delete_flag': 'Delete User',
            'active_flag':'Active User',
            'death_flag':'User Expired',
            'receipt_flag': 'User Premium',
            'receipt_no':'Receipt No',
            'receipt_date':'Receipt Date',
            'receipt_amt':'Receipt Amount',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'father_or_husband_name':forms.TextInput(attrs={'class':'form-control'}),
            'surname':forms.TextInput(attrs={'class':'form-control'}),
            'mother_name':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(choices=Gender,attrs={'class':'form-control form-select'}),
            'birth_date':DateInput(attrs={'class':'form-control'}),
            'mobile_no1':forms.TextInput(attrs={'class':'form-control'}),
            'mobile_no2':forms.TextInput(attrs={'class':'form-control'}),
            'area':forms.Select(attrs={'class':'form-control form-select'}),
            'village':forms.Select(attrs={'class':'form-control form-select'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'pincode':forms.TextInput(attrs={'class':'form-control'}),
            'occupation':forms.TextInput(attrs={'class':'form-control'}),
            'country':forms.TextInput(attrs={'class':'form-control','disabled': True}),
            'state':forms.TextInput(attrs={'class':'form-control','disabled': True}),
            'email_id':forms.TextInput(attrs={'class':'form-control'}),
            'delete_flag': forms.Select(choices=choice,attrs={'class':'form-control form-select'}),
            'active_flag':forms.Select(choices=choice,attrs={'class':'form-control form-select'}),
            'death_flag':forms.Select(choices=choice,attrs={'class':'form-control form-select'}),
            'receipt_flag':forms.Select(choices=choice,attrs={'class':'form-control form-select'}),
            'receipt_no':forms.TextInput(attrs={'class':'form-control'}),
            'receipt_date':DateInput(attrs={'class':'form-control'}),
            'receipt_amt':forms.TextInput(attrs={'class':'form-control'}),
        }

class Add_Premium_User_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Premium_User_Table
        fields = ['name','father_or_husband_name','surname','mobile_no1','mobile_no2','birth_date',
                    'address','area','village']
        labels = { 
            'usercode': 'User Code',
            'name':'Name *',
            'father_or_husband_name':'Father/Middle Name',
            'surname':'Surname *',
            'birth_date':'Birth Date',
            'mobile_no1':'Mobile Number',
            'mobile_no2':'Mobile Number 2',
            'address':'Address',
            'area':'Area *',
            'village':'Village *',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'father_or_husband_name':forms.TextInput(attrs={'class':'form-control'}),
            'surname':forms.TextInput(attrs={'class':'form-control'}),
            'birth_date':DateInput(attrs={'class':'form-control'}),
            'mobile_no1':forms.TextInput(attrs={'class':'form-control'}),
            'mobile_no2':forms.TextInput(attrs={'class':'form-control'}),
            'area':forms.Select(attrs={'class':'form-control form-select'}),
            'village':forms.Select(attrs={'class':'form-control form-select'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
        }


class Update_Premium_User_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Premium_User_Table

        ordering = ['id']
        
        fields = ['name','father_or_husband_name','surname','mobile_no1','mobile_no2','birth_date',
                    'address','area','village', 'death_flag', 'receipt_no', 'receipt_date']
        labels = { 
            'name':'Name *',
            'father_or_husband_name':'Father/Middle Name',
            'surname':'Surname *',
            'birth_date':'Birth Date',
            'mobile_no1':'Mobile Number',
            'mobile_no2':'Mobile Number 2',
            'address':'Address',
            'area':'Area *',
            'village':'Village *',
            'death_flag':'Expired',
            'receipt_no':'Receipt No',
            'receipt_date':'Receipt Date',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'father_or_husband_name':forms.TextInput(attrs={'class':'form-control'}),
            'surname':forms.TextInput(attrs={'class':'form-control'}),
            'birth_date':DateInput(attrs={'class':'form-control'}),
            'mobile_no1':forms.TextInput(attrs={'class':'form-control'}),
            'mobile_no2':forms.TextInput(attrs={'class':'form-control'}),
            'area':forms.Select(attrs={'class':'form-control form-select'}),
            'village':forms.Select(attrs={'class':'form-control form-select'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'death_flag':forms.Select(choices=choice,attrs={'class':'form-control form-select'}),
            'receipt_no':forms.TextInput(attrs={'class':'form-control'}),
            'receipt_date':DateInput(attrs={'class':'form-control'})
        }

