from django.shortcuts import render

# Create your views here.
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.db.models import Q
from django.http import JsonResponse
from .models import *
from django.shortcuts import render, redirect
from .forms import AdmissionForm, DropdownForm,TieupPageForm,SessionPageForm,DiscontinueForm,EnquiryForm,AdmissionFormPage
from twilio.rest import Client
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.db.models import Sum
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import StudentEnquiry
# Create your views here.

def index(request):
    return render(request, 'index.html')


def test(request):
    lag_report = StudentAdmission.objects.all()
    return render(request, "enquiry_report.html", {'lag_report': lag_report})
    # return render(request, 'test.html')


def report(request):
    return render(request, 'report_home.html')


def addon_home(request):
    return render(request, 'addon_home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'invaid credentials')
            return redirect('login')

    return render(request, 'login.html')


def enquiry_form(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            contact = form.cleaned_data.get('contact')  # Get the 'contact' field from the form data

            account_sid = 'ACdab8bd7b2266af37a154114131980357'
            auth_token = '7f51c0094f514af1a09657bcf3a0d090'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body="Greetings from Gtec Perumbavoor, Thanks for your enquiry. We will reach you Soon",
                from_='+12546169357',
                to='+91' + str(contact),
            )

            print(message.sid)
            # return redirect('success_url')
    else:
        form = EnquiryForm()
    return render(request, 'enquiry_form.html', {'form': form})




def admission_form(request):
    if request.method == 'POST':
        form = AdmissionFormPage(request.POST)
        if form.is_valid():
            stud_contact = form.cleaned_data['stud_contact']
            form.save()
            account_sid = 'ACdab8bd7b2266af37a154114131980357'
            auth_token = '7f51c0094f514af1a09657bcf3a0d090'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=" Welcome to Gtec Perumbavoor, Your admission has been confirmed.",
                from_='+12546169357',
                to='+91' + str(stud_contact),
            )

            print(message.sid)
    # return render(request, "admissionform.html", {'reg1': reg1})
    else:
        form = AdmissionFormPage()
    # return render(request, 'enquiry_form.html', {'form': form})
    return render(request, 'admissionform.html', {'form': form})

#
# def enq_details(request):
#     report = StudentEnquiry.objects.all()
#     return render(request, "enquiry_report.html", {'report': report})


# def enq_details(request):
#     # Get the current month and year
#     now = datetime.now()
#     current_month = now.month
#     current_year = now.year
#
#     # Filter StudentEnquiry objects to get inquiries for the current month
#     report = StudentEnquiry.objects.filter(enq_date__month=current_month, enq_date__year=current_year)
#
#     return render(request, "enquiry_report.html", {'report': report})




def enq_details(request):
    # Get the current month and year
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # Set the default start and end dates to the current month
    start_date = datetime(current_year, current_month, 1).date()
    end_date = datetime(current_year, current_month + 1, 1).date() - timedelta(days=1)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            # Handle the case where the date format is incorrect
            pass

    report = StudentEnquiry.objects.filter(enq_date__range=[start_date, end_date])

    return render(request, "enquiry_report.html", {'report': report, 'start_date': start_date, 'end_date': end_date})




def delete(request, taskid):
    done = StudentEnquiry.objects.get(id=taskid)
    if request.method == 'POST':
        done.delete()
        return redirect('admission_form')
    return render(request, "delete.html")


def stud_report(request):
    stud_report = Admission.objects.filter(
        Q(certificate_status__certificate='Not Received') & Q(student_status__Student_status='Running'))
    return render(request, "student_report.html", {'stud_report': stud_report})


def old_stud_report(request):
    old_stud_report = Admission.objects.filter(
        Q(certificate_status__in=[2,3]) | Q(student_status=3))
    return render(request, "old_student_report.html", {'old_stud_report': old_stud_report})

def discontinue_report(request):
    discontinue_report = Discontinue.objects.all()
    return render(request, "discontinue_report.html", {'discontinue_report': discontinue_report})

def exam_report(request):
    exam_report = StudentAdmission.objects.all()
    return render(request, "exam_report.html", {'exam_report': exam_report})


def update(request, id):
    stud_update = Admission.objects.get(id=id)
    f = AdmissionFormPage(request.POST or None, instance=stud_update)
    if f.is_valid():
        f.save()
        return redirect('stud_report')
    return render(request, 'edit.html', {'f': f, 'stud_update': stud_update})



def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'

    # Query all student report data
    student_reports = Admission.objects.filter(certificate_status__in=[1])

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    # Define the data for the table
    data = [['Reg No', 'Student Name', 'Parent Name', 'Parent Contact', 'Address',
             'Contact Number', 'Qualification', 'Dob', 'Gender', 'Course 1',
             'Course 3', 'Duration', 'Scheme', 'Fee', 'Joining Date', 'Exam Date', 'Certificate Status']]

    for report in student_reports:
        data.append([report.regno, report.stud_name, report.parent_name, report.parent_contact,
                     report.stud_address, report.stud_contact, report.qualification,
                     report.dob, report.gender, report.course,  report.student_status,
                     report.course_duration, report.scheme, report.fee, report.joining_date,
                     report.exam_date, report.certificate_status])

    # Create the table and style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
        ('FONTSIZE', (0, 0), (-1, -1), 6)
    ]))

    # Add the table to the PDF
    elements.append(table)

    # Build the PDF document
    doc.build(elements)

    return response


def logout(request):
    return render(request, 'login.html')


def addon_clg(request):
    clg = Add_collage.objects.all()
    if request.method == "POST":
        clg_name = request.POST.get('clg_name', '')
        collage = Add_collage(name=clg_name)
        collage.save()
    return render(request, "addon_clg.html", {'clg': clg})


def addon_staff(request):
    staff = Add_staff.objects.all()
    if request.method == "POST":
        staff_name = request.POST.get('staff_name', '')
        staff = Add_staff(name=staff_name)
        staff.save()
    return render(request, "addon_staff.html", {'staff': staff})


def addon_course(request):
    course = Add_course.objects.all()
    if request.method == "POST":
        course_name = request.POST.get('course_name', '')
        course = Add_course(name=course_name)
        course.save()
    return render(request, "addon_course.html", {'course': course})


def addon_scheme(request):
    scheme = Add_scheme.objects.all()
    if request.method == "POST":
        scheme_name = request.POST.get('scheme_name', '')
        scheme = Add_scheme(name=scheme_name)
        scheme.save()
    return render(request, "addon_scheme.html", {'scheme': scheme})


def tieup_page(request):
    if request.method == 'POST':
        form = TieupPageForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success_url')
    else:
        form = TieupPageForm()

    return render(request, 'tieup_form.html', {'form': form})

def session_form(request):
    if request.method == 'POST':
        form = SessionPageForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success_url')
    else:
        form = SessionPageForm()
    return render(request, 'session_form.html', {'form': form})




def session_report(request):
    sessions = Session.objects.all()
    tieups = Tieup.objects.all()

    for tieup in tieups:
        used_duration = Session.objects.filter(college=tieup.college, course=tieup.course).aggregate(total_duration=Sum('duration'))['total_duration']
        tieup.used_duration = used_duration if used_duration else 0
        tieup.remaining_duration = tieup.course_duration - tieup.used_duration

    context = {'sessions': sessions, 'tieups': tieups}
    return render(request, 'session_report.html', context)



def tieup_report(request):
    tieup_report = Tieup.objects.all()
    return render(request, "tieup_report.html", {'tieup_report': tieup_report})


def discontinue_form(request):
    form = DiscontinueForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            admission_instance = Admission.objects.get(regno=form.cleaned_data['regno'])
            student_status_instance = Student_status.objects.get(id=3)  # Assuming '1' is the ID of the 'Discontinue' status
            admission_instance.student_status = student_status_instance
            admission_instance.save()
            # Redirect or show a success message

    return render(request, 'discontinue_form.html', {'form': form})


#
# def discontinue_form(request):
#     if request.method == 'POST':
#         form = DiscontinueForm(request.POST)
#
#         if form.is_valid():
#             regno = form.cleaned_data['regno']
#             try:
#                 admission_instance = Admission.objects.get(regno=regno)
#                 student_status_instance = Student_status.objects.get(id=3)  # Assuming '3' is the ID of the 'Discontinue' status
#                 admission_instance.student_status = student_status_instance
#                 admission_instance.save()
#
#                 # Fetch student's name and course
#                 student_name = admission_instance.student.name
#                 course = admission_instance.student.course
#
#                 return render(request, 'discontinue_form.html', {'form': form, 'student_name': student_name, 'course': course})
#
#             except Admission.DoesNotExist:
#                 error_message = "Invalid registration number. Please try again."
#                 return render(request, 'discontinue_form.html', {'form': form, 'error_message': error_message})
#
#     else:
#         form = DiscontinueForm()
#
#     return render(request, 'discontinue_form.html', {'form': form})







def start_exam(request):
    if request.method == 'POST':
        reg_no = request.POST.get('reg_no')
        try:
            student = Admission.objects.get(regno=reg_no)
            return redirect('take_exam', course=student.course)
        except Admission.DoesNotExist:
            return render(request, 'error.html', {'error_message': 'Invalid registration number'})
    return render(request, 'start_exam.html')


def take_exam(request, course):
    google_form_links = {
        'PYTHON': 'https://forms.gle/D6Hn7K2HtZbLjMVz7',
        'CPP': 'https://forms.gle/mQ3SWcaHAjAaijgu8',
        'JAVA': 'https://forms.gle/mQ3SWcaHAjAaijgu8',
    }
    # return redirect(google_form_links[course])
    return redirect(google_form_links.get(course, '/'))

