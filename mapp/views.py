from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
import re, csv
from copy import deepcopy
from django.contrib import messages
from django.core.paginator import Paginator
from .filters import *
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    PageBreak,
)

def download_sticker_pdf(request, filterr, table_data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="user.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4, title="Download Sticker")
    elements = []
    if table_data == "Main_User_Table":
      data_table = Main_User_Table
    else:
      data_table = Premium_User_Table
    # Define the style for the table
    style_table = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (-1, 0), (0, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 7, colors.gray),
        ('GRID', (0, 0), (-1, -1), 7, colors.whitesmoke),
        ('TOPPADDING', (0, 0), (-1, -1), 15),  # Add top padding to cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),  # Add bottom padding to cells
        ('LEFTPADDING', (0, 0), (-1, -1), 15),  # Add left padding to cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),  # Add right padding to cells
    ])

    custom_style = ParagraphStyle(
        name='custom_style',
        parent=getSampleStyleSheet()['Normal'],
        fontName='Helvetica',
        fontSize=13,
    )

    lines = []
    main_data = []

    if len(filterr) > 2:
        filtered_data_csv = filterr[1:-1].split(', ')
        order_by_field = 'area__area_name' if filtered_data_csv[-1] == "'area'" else 'village__village_name'
        filtered_data_csv = data_table.objects.filter(pk__in=filtered_data_csv[0:-1]).order_by(order_by_field)
        # are_vil_flag = None
        for i in filtered_data_csv:
            name = i.name + ' ' + i.father_or_husband_name + ' ' + i.surname
            village_name = "Village: " + i.village.village_name
            Area_name = "Area: " + i.area.area_name.capitalize()
            if table_data == "Main_User_Table":
              address_lines = Paragraph(
                  "Usercode: " + i.usercode + " <b>" + " <br/>" + name + "</b> " + " <br/>" +
                  i.address + ' ' + i.state + " " + " <br/>" +
                  "Mobile: " + i.mobile_no1 + ' / ' + i.mobile_no2 + " <br/>" +
                  "Pincode: " + i.pincode + " <br/>" +
                  "<b>" + Area_name + "</b>" + " <br/>" +
                  village_name ,
                  custom_style
              )
            else:
              address_lines = Paragraph(
                        "<b>" + name + "</b> " +  " <br/>" +
                        i.address + ' <br/>' +
                        "Mobile: " + i.mobile_no1 + ' / ' + i.mobile_no2 + " <br/>" +
                        "<b>" + Area_name + "</b>" + " <br/>" +
                        village_name,
                        custom_style
                    )

  
            if len(lines) == 0 or len(lines[-1]) == 2:
                lines.append([address_lines])
            else:
                lines[-1].append(address_lines)

        main_data.append(lines[:])

    for idx, table in enumerate(main_data):
        col_widths = [270]
        table1 = Table(table, colWidths=col_widths, repeatRows=1)
        table1.setStyle(style_table)
        elements.append(table1)

        if idx < len(main_data) - 1:
            elements.append(PageBreak())

    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return response


def download_split_sticker_pdf(request, filterr, table_data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="user.pdf"'
    if table_data == "Main_User_Table":
      data_table = Main_User_Table
    else:
      data_table = Premium_User_Table
    doc = SimpleDocTemplate(response, pagesize=A4, title="Download Sticker")
    elements = []

    # Define the style for the table
    style_table = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 7, colors.gray),
        ('GRID', (0, 0), (-1, -1), 7, colors.whitesmoke),
        ('TOPPADDING', (0, 0), (-1, -1), 15),  # Add top padding to cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),  # Add bottom padding to cells
        ('LEFTPADDING', (0, 0), (-1, -1), 15),  # Add left padding to cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),  # Add right padding to cells
    ])

    custom_style = ParagraphStyle(
        name='custom_style',
        parent=getSampleStyleSheet()['Normal'],
        fontName='Helvetica',
        fontSize=13,
    )

    lines = []
    main_data = []

    if len(filterr) > 2:
        filtered_data_csv = filterr[1:-1].split(', ')
        order_by_field = 'area__area_name' if filtered_data_csv[-1] == "'area'" else 'village__village_name'
        filtered_data_csv = data_table.objects.filter(pk__in=filtered_data_csv[0:-1]).order_by(order_by_field)
        are_vil_flag = None
        for i in filtered_data_csv:
            if order_by_field == 'area__area_name':
                if are_vil_flag is None:
                    are_vil_flag = i.area.area_name
                elif are_vil_flag != i.area.area_name:
                    main_data.append(lines[:])
                    lines.clear()
                    are_vil_flag = i.area.area_name
            else:
                if are_vil_flag is None:
                    are_vil_flag = i.village.village_name
                elif are_vil_flag != i.village.village_name:
                    main_data.append(lines[:])
                    lines.clear()
                    are_vil_flag = i.village.village_name

            name = i.name + ' ' + i.father_or_husband_name + ' ' + i.surname
            village_name = "Village: " + i.village.village_name
            Area_name = "Area: " + i.area.area_name.capitalize()
            if table_data == "Main_User_Table":
              address_lines = Paragraph(
                  "Usercode: " + i.usercode + " <b>" + " <br/>" + name + "</b> " + " <br/>" +
                  i.address + ' ' + i.state + " " + " <br/>" +
                  "Mobile: " + i.mobile_no1 + ' / ' + i.mobile_no2 + " <br/>" +
                  "Pincode: " + i.pincode + " <br/>" +
                  "<b>" + Area_name + "</b>" + " <br/>" +
                  village_name ,
                  custom_style
              )
            else:
               address_lines = Paragraph(
                        "<b>" + name + "</b> " +  " <br/>" +
                        i.address + ' <br/>' +
                        "Mobile: " + i.mobile_no1 + ' / ' + i.mobile_no2 + " <br/>" +
                        "<b>" + Area_name + "</b>" + " <br/>" +
                        village_name,
                        custom_style
                    )
            if len(lines) == 0 or len(lines[-1]) == 2:
                lines.append([address_lines])
            else:
                lines[-1].append(address_lines)

        main_data.append(lines[:])

    for idx, table in enumerate(main_data):
        col_widths = [270]
        table1 = Table(table, colWidths=col_widths, repeatRows=1)
        table1.setStyle(style_table)
        elements.append(table1)

        if idx < len(main_data) - 1:
            elements.append(PageBreak())

    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return response

def add_page_number(canvas, doc):
    page_number = canvas.getPageNumber()
    text = "Page {}".format(page_number)
    canvas.setFont("Helvetica", 12)
    canvas.drawCentredString(A4[0] / 2, 1.25 * cm, text)


def download_pdf(request, filterr, table_data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="user.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4, title="Download PDF")
    elements = []
    if table_data == "Main_User_Table":
      data_table = Main_User_Table
      table_head = ["Usercode", 'Member Name', 'Mobile No.', 'Area', 'Address', 'Remark 1']
      lines1 = [["Usercode", 'Member Name', 'Mobile No.', 'Area', 'Address', 'Remark 1']]
    else:
      data_table = Premium_User_Table
      table_head = ['Member Name', 'Mobile No.', 'Area', 'Address', 'Remark 1']
      lines1 = [['Member Name', 'Mobile No.', 'Area', 'Address', 'Remark 1']]


    # Define the style for the table
    style_table = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    style_table.add('FONTSIZE', (0, 0), (-1, 0), 10)
    normal_style = getSampleStyleSheet()['Normal']
    # Increase the font size
    normal_style.fontSize += 1
    # Define the data for the table
    lines = []
    main_data = []
    if len(filterr) > 2:
        filtered_data_csv = filterr[1:-1].split(', ')
        order_by_field = 'area__area_name' if filtered_data_csv[-1] == "'area'" else 'village__village_name'
        filtered_data_csv = data_table.objects.filter(pk__in=filtered_data_csv[0:-1]).order_by(order_by_field)
        are_vil_flag = None
        for i in filtered_data_csv:
          if order_by_field == 'area__area_name':
            if are_vil_flag is None:
                  are_vil_flag = i.area.area_name
            elif are_vil_flag != i.area.area_name:
                lines.insert(0, table_head)
                main_data.append(deepcopy(lines))
                lines.clear()
                are_vil_flag = i.area.area_name
          else:
            if are_vil_flag is None:
                  are_vil_flag = i.village.village_name
            elif are_vil_flag != i.village.village_name:
                lines.insert(0, table_head)
                main_data.append(deepcopy(lines))
                lines.clear()
                are_vil_flag = i.village.village_name
            # Split long lines of text into multiple lines using the Paragraph class
          if table_data == "Main_User_Table":
            usercode = Paragraph(i.usercode, normal_style)
            address_lines = Paragraph(i.address + ' ' + i.pincode + ' ' + i.state, normal_style)
            member_name = Paragraph(i.name + ' ' + i.father_or_husband_name + ' ' + i.surname, normal_style)
            area_name = Paragraph(i.area.area_name, normal_style)
            mobile_no = Paragraph(i.mobile_no1 + ' ' + i.mobile_no2, normal_style)
            lines.append([usercode, member_name, mobile_no, area_name, address_lines, ''])
          else:
            address_lines = Paragraph(i.address, normal_style)
            member_name = Paragraph(i.name + ' ' + i.father_or_husband_name + ' ' + i.surname, normal_style)
            area_name = Paragraph(i.area.area_name, normal_style)
            mobile_no = Paragraph(i.mobile_no1 + ' ' + i.mobile_no2, normal_style)
            lines.append([member_name, mobile_no, area_name, address_lines, ''])
        lines.insert(0, table_head)
        main_data.append(deepcopy(lines))

    # Set the column widths to fixed values
    print(lines1)
    for table in main_data:
        if table_data == "Main_User_Table":
          col_widths = [90, 85, 80, 70, 140, 65]
        else:
          col_widths = [85, 80, 70, 140, 65]
        table1 = Table(table, colWidths=col_widths, repeatRows=1)
        table1.setStyle(style_table)
        # Add the table to the elements list
        elements.append(table1)
        elements.append(PageBreak())

    # Call the add_page_number function for page numbering
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

    return response 

def download_csv(request, filterr, table_data):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=user.csv'
    writer = csv.writer(response)
    if table_data == "Main_User_Table":
      data_table = Main_User_Table
      writer.writerow(['Member ID', 'Member Name', 'Mobile number 1', 'Area', 'Village', 'Address', 'Remark 1', 'Remark 2'])
    else:
      data_table = Premium_User_Table
      writer.writerow(['Member Name', 'Mobile number 1', 'Area', 'Village', 'Address', 'Remark 1', 'Remark 2'])

    if len(filterr) > 2:
        filtered_data_csv = filterr[1:-1].split(', ')
        order_by_field = 'area__area_name' if filtered_data_csv[-1] == "'area'" else 'village__village_name'
        filtered_data_csv = data_table.objects.filter(pk__in=filtered_data_csv[0:-1]).order_by(order_by_field)

        for i in filtered_data_csv:
            if table_data == "Main_User_Table":
              member_name = i.name + ' ' + i.father_or_husband_name + ' ' + i.surname
              address = i.address + ' ' + i.pincode + ' ' + i.state
              writer.writerow([i.usercode, member_name, i.mobile_no1, i.area.area_name, i.village.village_name, address, '', ''])
            else:
              member_name = i.name + ' ' + i.father_or_husband_name + ' ' + i.surname
              address = i.address 
              writer.writerow([member_name, i.mobile_no1, i.area.area_name, i.village.village_name, address, '', ''])

    return response


def print_user(request):
        head = ['User Code','Name','Middle Name','Surname','Area','Village','Mobile No 1','Mobile No 2','Address','Active Status']
        if request.GET.get('filter')=='village' and len(request.GET)>1:
            vil_id = dict(request.GET)['filter_village_area_id']
            usertable = Main_User_Table.objects.filter(village__in=vil_id).order_by('village__village_name')
            downlaod_value = sorted(list(usertable.values_list('id',flat=True)))
            downlaod_value.append('village')
        elif request.GET.get('filter')=='area' and len(request.GET)>1:
            are_id = dict(request.GET)['filter_village_area_id']
            usertable = Main_User_Table.objects.filter(area__in=are_id).order_by('area__area_name')
            downlaod_value = list(usertable.values_list('id',flat=True))
            downlaod_value.append('area')
        else:
          if request.GET.get('filter')=='area':
            usertable = Main_User_Table.objects.all().order_by('area__area_name')
            downlaod_value = sorted(list(usertable.values_list('id',flat=True)))
            downlaod_value.append('area')
          else:
            usertable = Main_User_Table.objects.all().order_by('village__village_name')
            downlaod_value = sorted(list(usertable.values_list('id',flat=True)))
            downlaod_value.append('village')
        return render(request, 'staff/download.html', {'usertable':usertable, 'head':head, 'downlaod_value': downlaod_value, 'table_data1':"Main_User_Table"})

def ajax_load_data(request):
    filter_with = request.GET.get('filter')
  
    if filter_with == "village":
        filter_val = Village.objects.all().order_by("village_name")
    elif filter_with == "area":
        filter_val = Area.objects.all().order_by("area_name")
    else:
        filter_val = None
    return render(request, 'staff/dropd.html', {'filter_val': filter_val, 'filter_with': filter_with})


def staff_login(request):
  try:
    if not request.user.is_authenticated:
      if request.method == 'POST':
          fm = Login_Form(request=request, data=request.POST)
          if fm.is_valid():
            nm = fm.cleaned_data['username']
            ps = fm.cleaned_data['password']
            staff = authenticate(username=nm, password=ps)
            if staff is not None:
              login(request, staff)
              return HttpResponseRedirect('/profile/')
      else:
          fm = Login_Form('/mapp/') 
      return render(request, 'staff/staff_login.html', {'auth_form': fm})
    else:
      return HttpResponseRedirect('/profile/')
  except Exception as e:
      print("exceptionnnnnnn", e)
     
def staff_logout(request):
  try:
    logout(request)
    return HttpResponseRedirect('/')
  except Exception as e:
    print("exceptionnnnnnn", e)

def profile(request):
  try:
    if request.user.is_authenticated:
      total_counts = {
         "user_count":Main_User_Table.objects.count(),
         "village_count":Village.objects.count(),
         "area_count":Area.objects.count()
         }
      return render(request, 'staff/profile.html', total_counts)
    else:
      return HttpResponseRedirect('/')
  except Exception as e:
    print("exceptionnnnnnn", e)
  
def add_user(request):
    if request.method == 'POST':
      s_form = Add_User_Form(request.POST)
      if s_form.is_valid():
        s_form.save()
        messages.success(request, 'User Added!')
        s_form = Add_User_Form()
        usr_id = Main_User_Table.objects.latest('created_date').id
        usr_nam = Main_User_Table.objects.get(pk=usr_id).name
        try:
          vil_id = Main_User_Table.objects.get(pk=usr_id).village_id
          vil_nam = Village.objects.get(pk=vil_id).village_name
          usr_in_village_update = Village.objects.get(pk=vil_id).usr_in_village
          Village.objects.filter(id=vil_id).update(usr_in_village=int(usr_in_village_update)+1)
          usr_in_village_update = Village.objects.get(pk=vil_id).usr_in_village
          usr_code = vil_nam+'-'+str(usr_in_village_update)+'-'+str(usr_id)
          print(usr_code)
          Main_User_Table.objects.filter(id=usr_id).update(usercode=usr_code)
        except Exception as e:
          print("exceptionnnnnnn", e)
    else:
      s_form = Add_User_Form()
    return render(request, 'staff/add_user.html', {'add_user_form': s_form})


def update_user(request, id):
  try:
    if request.method == 'POST':
      up = Main_User_Table.objects.get(pk=id)
      updateclass = Update_User_Form(request.POST, instance=up)
      if updateclass.is_valid():
        updateclass.save()
        messages.success(request, 'User detail has been Updated!')
        updateclass = Update_User_Form()
    else:
      up = Main_User_Table.objects.get(pk=id)
    updateclass = Update_User_Form(instance=up)
    return render(request, 'staff/update.html', {'updateclass':updateclass, 'update_head':'Update User', 'update_back_btn':'/show_user/'})
  except Exception as e:
    print("exceptionnnnnnn", e)

def show_user(request):
    try:
        head = ['User Code','Name','Middle Name','Surname','Area','Village','Mobile No 1','Mobile No 2','Address','Active Status']
        usertable = Main_User_Table.objects.all().select_related()

        myfilter = OderFilter(request.GET, queryset=usertable)
        usertable = myfilter.qs
        paginator = Paginator(usertable, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Calculate the range of page numbers to display
        if paginator.num_pages <= 3:
            # If there are 5 or fewer pages, display all of them
            page_range = range(1, paginator.num_pages + 1)
        else:
            # Otherwise, display the current page plus 2 pages before and after
            current_index = page_obj.number - 1
            start_index = max(0, current_index - 2)
            end_index = min(paginator.num_pages - 1, current_index)
            if end_index - start_index < 4:
                if start_index == 0:
                    end_index = min(end_index + 4 - (end_index - start_index), paginator.num_pages - 1)
                else:
                    start_index = max(start_index - (4 - (end_index - start_index)), 0)
            page_range = range(start_index + 1, end_index)
        return render(request, 'staff/show_user.html', {'usertable':page_obj, 'head':head, 'page_range':page_range, 'myfilter':myfilter})
    except Exception as e:
        print("exceptionnnnnnn", e)


def add_village(request):
  try:
    if request.method == 'POST':
      formclass = Village_Form(request.POST)
      if formclass.is_valid():
        village_name= formclass.cleaned_data['village_name']
        name_already_present = False
        special_char = False
        if re.match("^[A-Za-z0-9() ._-]*$", village_name) == None:
           special_char = True
           messages.error(request, 'Only numbers and alphabets are allowed!')
        if special_char == False:
          for i in Village.objects.all().values():
            if i['village_name'].upper() == village_name.upper():
              messages.error(request, 'Village is already present!')
              name_already_present =True
              break
        if name_already_present == False and special_char == False:
          formclass.save()
          messages.success(request, 'Village Added')
          vil_id = Village.objects.latest('created_date').id
          vil_nam = Village.objects.get(pk=vil_id).village_name
          formclass = Village_Form()
    else:
      formclass = Village_Form()
    userview = Village.objects.all()
    paginator = Paginator(userview, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate the range of page numbers to display
    if paginator.num_pages <= 3:
        # If there are 5 or fewer pages, display all of them
        page_range = range(1, paginator.num_pages + 1)
    else:
        # Otherwise, display the current page plus 2 pages before and after
        current_index = page_obj.number - 1
        start_index = max(0, current_index - 2)
        end_index = min(paginator.num_pages - 1, current_index)
        if end_index - start_index < 4:
            if start_index == 0:
                end_index = min(end_index + 4 - (end_index - start_index), paginator.num_pages - 1)
            else:
                start_index = max(start_index - (4 - (end_index - start_index)), 0)
        page_range = range(start_index + 1, end_index)
    return render(request, 'staff/add_village.html', {'formclass':formclass, 'userview':page_obj, 'page_range':page_range})
  except Exception as e:
    print("exceptionnnnnnn", e)

def update_village(request, id):
  try:
    if request.method == 'POST':
      up = Village.objects.get(pk=id)
      updateclass = Village_Form(request.POST, instance=up)
      if updateclass.is_valid():
        #this code is to only alpha numeric values and non repeatative name 
        village_name= updateclass.cleaned_data['village_name']
        name_already_present = False
        special_char = False
        if re.match("^[A-Za-z0-9(). _-]*$", village_name) == None:
          special_char = True
          messages.error(request, 'Only numbers and alphabets are allowed!')
        if special_char == False:
          for i in Village.objects.all().values():
            if i['village_name'].upper() == village_name.upper():
              messages.error(request, 'Village is already present!')
              name_already_present =True
              break
        if name_already_present == False and special_char == False:
          updateclass.save()
          messages.success(request, 'village has been Updated!')

          #below code is to update the usercode initial village name
          if int(up.usr_in_village)>0:
            user_have_village = Main_User_Table.objects.filter(village_id=id)
            usercode_old_village_name = 0
            for i in user_have_village:
              updated_usercode_name = i.usercode.split('-')
              usercode_old_village_name = updated_usercode_name[0]
              updated_usercode_name[0] = up.village_name
              break
            updated_usercode_name = '-'.join(updated_usercode_name)
            Main_User_Table.objects.filter(usercode__startswith=usercode_old_village_name).update(usercode=updated_usercode_name)
          updateclass = Village_Form()
    else:
      up = Village.objects.get(pk=id)
      updateclass = Village_Form(instance=up)
    return render(request, 'staff/update.html', {'updateclass':updateclass, 'update_head':'Update Village', 'update_back_btn':'/add_village/'})
  except Exception as e:
    print("exceptionnnnnnn", e)


def add_area(request):
  try:
    if request.method == 'POST':
      formclass = Area_Form(request.POST)
      if formclass.is_valid():
        area_name= formclass.cleaned_data['area_name']
        name_already_present = False
        special_char = False
        if re.match("^[A-Za-z0-9(). _-]*$", area_name) == None:
           special_char = True
           messages.error(request, 'Only numbers and alphabets are allowed!')
        if special_char == False:
          for i in Area.objects.all().values():
            if i['area_name'].upper() == area_name.upper():
              messages.error(request, 'Area is already present!')
              name_already_present =True
              break
        if name_already_present == False and special_char == False:
          formclass.save()
          messages.success(request, 'Area Added')
          area_id = Area.objects.latest('created_date').id
          area_nam = Area.objects.get(pk=area_id).area_name
          formclass = Area_Form()
    else:
      formclass = Area_Form()
    userview = Area.objects.all()
    paginator = Paginator(userview, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate the range of page numbers to display
    if paginator.num_pages <= 3:
        # If there are 5 or fewer pages, display all of them
        page_range = range(1, paginator.num_pages + 1)
    else:
        # Otherwise, display the current page plus 2 pages before and after
        current_index = page_obj.number - 1
        start_index = max(0, current_index - 2)
        end_index = min(paginator.num_pages - 1, current_index)
        if end_index - start_index < 4:
            if start_index == 0:
                end_index = min(end_index + 4 - (end_index - start_index), paginator.num_pages - 1)
            else:
                start_index = max(start_index - (4 - (end_index - start_index)), 0)
        page_range = range(start_index + 1, end_index)
    return render(request, 'staff/add_area.html', {'formclass':formclass, 'userview':page_obj, 'page_range':page_range})
  except Exception as e:
    print("exceptionnnnnnn", e)

def update_area(request, id):
  try:
    if request.method == 'POST':
      up = Area.objects.get(pk=id)
      updateclass = Area_Form(request.POST, instance=up)
      if updateclass.is_valid():
        area_name= updateclass.cleaned_data['area_name']
        name_already_present = False
        special_char = False
        if re.match("^[A-Za-z0-9() ._-]*$", area_name) == None:
           special_char = True
           messages.error(request, 'Only numbers and alphabets are allowed!')
        if special_char == False:
          for i in Area.objects.all().values():
            if i['area_name'].upper() == area_name.upper():
              messages.error(request, 'Area is already present!')
              name_already_present =True
              break
        if name_already_present == False and special_char == False:
          updateclass.save()
          messages.success(request, 'Area has been Updated!')
          updateclass = Area_Form() 
    else:
      up = Area.objects.get(pk=id)
      updateclass = Area_Form(instance=up)
    return render(request, 'staff/update.html', {'updateclass':updateclass, 'update_head':'Update Area', 'update_back_btn':'/add_area/'})
  except Exception as e:
    print("exceptionnnnnnn", e)


#####################################################****** premium *****########################################################################
def premium_profile(request):
  return render(request, 'premium/premium_profile.html')

def add_premium_user(request):
    if request.method == 'POST':
      s_form = Add_Premium_User_Form(request.POST)
      if s_form.is_valid():
        s_form.save()
        messages.success(request, 'User Added!')
        s_form = Add_Premium_User_Form()
    else:
      s_form = Add_Premium_User_Form()
    return render(request, 'premium/add_premium_user.html', {'add_premium_user_form': s_form})

def update_premium_user(request, id):
  try:
    if request.method == 'POST':
      up = Premium_User_Table.objects.get(pk=id)
      updateclass = Update_Premium_User_Form(request.POST, instance=up)
      if updateclass.is_valid():
        updateclass.save()
        messages.success(request, 'User detail has been Updated!')
        updateclass = Update_Premium_User_Form()
    else:
      up = Premium_User_Table.objects.get(pk=id)
    updateclass = Update_Premium_User_Form(instance=up)
    return render(request, 'premium/update_premium.html', {'updateclass':updateclass, 'update_head':'Update User', 'update_back_btn':'/show_premium_user/'})
  except Exception as e:
    print("exceptionnnnnnn", e)
  
def show_premium_user(request):
    try:
        head = ['Name','Middle Name','Surname','Area','Village','Mobile No 1','Mobile No 2','Address', 'Expired', 'Receipt No', 'Receipt Date']
        usertable = Premium_User_Table.objects.all().select_related()
        myfilter = OderFilter(request.GET, queryset=usertable)
        usertable = myfilter.qs
        return render(request, 'premium/show_premium_user.html', {'usertable':usertable, 'head':head, 'myfilter':myfilter})
    except Exception as e:
        print("exceptionnnnnnn", e)

def print_premium_user(request):
        head = ['Name','Area','Village','Mobile No 1', 'Address', 'age','Expired', 'Receipt No', 'Receipt Date']
        if request.GET.get('filter')=='village' and len(request.GET)>1:
            vil_id = dict(request.GET)['filter_village_area_id']
            usertable = Premium_User_Table.objects.filter(village__in=vil_id).order_by('village__village_name')
            downlaod_value = sorted(list(usertable.values_list('id',flat=True)))
            downlaod_value.append('village')
        elif request.GET.get('filter')=='area' and len(request.GET)>1:
            are_id = dict(request.GET)['filter_village_area_id']
            usertable = Premium_User_Table.objects.filter(area__in=are_id).order_by('area__area_name')
            downlaod_value = list(usertable.values_list('id',flat=True))
            downlaod_value.append('area')
        else:
          if request.GET.get('filter')=='area':
            usertable = Premium_User_Table.objects.all().order_by('area__area_name')
            downlaod_value = sorted(list(usertable.values_list('id',flat=True)))
            downlaod_value.append('area')
          else:
            usertable = Premium_User_Table.objects.all().order_by('village__village_name')
            downlaod_value = sorted(list(usertable.values_list('id',flat=True)))
            downlaod_value.append('village')
        return render(request, 'premium/premium_download.html', {'usertable':usertable, 'head':head, 'downlaod_value': downlaod_value, 'table_data1':"Premium_User_Table"})