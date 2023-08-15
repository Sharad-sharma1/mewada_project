import django_filters

from .models import *
from .forms import *

class OderFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(label_suffix='', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
    father_or_husband_name = django_filters.CharFilter(label_suffix='', label='Middle Name',widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}),lookup_expr='icontains')
    area_id = django_filters.ModelChoiceFilter(label_suffix='', queryset=Area.objects.all(),label='Area', widget=forms.Select(attrs={'class':'form-select form-select-sm'}))
    village_id = django_filters.ModelChoiceFilter(label_suffix='',queryset=Village.objects.all(), label='Village', widget=forms.Select(attrs={'class':'form-select form-select-sm'}))
    mobile_no1 = django_filters.CharFilter(label_suffix='',label='Mobile No 1', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
    mobile_no2 = django_filters.CharFilter(label_suffix='',label='Mobile No 2', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
    death_flag = django_filters.CharFilter(label_suffix='',label='Expired', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
    receipt_no = django_filters.CharFilter(label_suffix='',label='Receipt No', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
    receipt_date = django_filters.CharFilter(label_suffix='',label='Receipt Date', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
    birth_date = django_filters.CharFilter(label_suffix='',label='Age', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')

    class Meta:
        model = Main_User_Table
        fields = ['name','father_or_husband_name','area_id','village_id', 'mobile_no1', 'mobile_no2', 'death_flag', 'receipt_no', 'receipt_date','birth_date']

# class OderFilter(django_filters.FilterSet):

#     name = django_filters.CharFilter(label_suffix='', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
#     father_or_husband_name = django_filters.CharFilter(label_suffix='', label='Middle Name',widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}),lookup_expr='icontains')
#     area_id = django_filters.ModelChoiceFilter(label_suffix='', queryset=Area.objects.all(),label='Area', widget=forms.Select(attrs={'class':'form-select form-select-sm'}))
#     village_id = django_filters.ModelChoiceFilter(label_suffix='',queryset=Village.objects.all(), label='Village', widget=forms.Select(attrs={'class':'form-select form-select-sm'}))
#     mobile_no1 = django_filters.CharFilter(label_suffix='',label='Mobile No 1', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
#     mobile_no2 = django_filters.CharFilter(label_suffix='',label='Mobile No 2', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')

#     class Meta:
#         model = Premium_User_Table
#         fields = ['name','father_or_husband_name','area_id','village_id', 'mobile_no1', 'mobile_no2']


# class DownloadFilterPremium(django_filters.FilterSet):
    
#     area_id = django_filters.ModelChoiceFilter(label_suffix='', queryset=Area.objects.all(),label='Area', widget=forms.Select(attrs={'class':'form-select form-select-sm', 'multiple': "true", 'multiselect-search':"true"}))
#     village_id = django_filters.ModelChoiceFilter(label_suffix='',queryset=Village.objects.all(), label='Village', widget=forms.Select(attrs={'class':'form-select form-select-sm', 'multiple': "true", 'multiselect-search':"true"}))
    # death_flag = django_filters.CharFilter(label_suffix='',label='Expired', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
    # receipt_no = django_filters.CharFilter(label_suffix='',label='Receipt No', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
    # receipt_date = django_filters.CharFilter(label_suffix='',label='Receipt Date', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')
    # birth_date = django_filters.CharFilter(label_suffix='',label='Age', widget=forms.TextInput(attrs={'class':'form-control form-control-sm '}),lookup_expr='icontains')

    
#     class Meta:
#         model = Premium_User_Table
#         fields = ['area_id','village_id', 'death_flag', 'receipt_no', 'receipt_date','birth_date']

# class DownloadFilter(django_filters.FilterSet):
    
#     area_id = django_filters.ModelChoiceFilter(label_suffix='', queryset=Area.objects.all(),label='Area', widget=forms.Select(attrs={'class':'form-select form-select-sm', 'multiple': "true", 'multiselect-search':"true"}))
#     village_id = django_filters.ModelChoiceFilter(label_suffix='',queryset=Village.objects.all(), label='Village', widget=forms.Select(attrs={'class':'form-select form-select-sm', 'multiple': "true", 'multiselect-search':"true"}))
    
#     class Meta:
#         model = Main_User_Table
#         fields = ['area_id','village_id']

