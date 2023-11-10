from django.shortcuts import render,redirect
from Student.models import Student,Tuition,Payment,Project,External_Tuition

from forms.add_student import StudentForm
from forms.project_edit import ProjectForm
from datetime import datetime
from django.db.models import Sum
import calendar
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from forms.add_instructor import InstructorRegistrationForm
from random import randint
from Instructor.models import Instructor
from Reservation.models import Reservation
from User.models import Contact,Notification,User
from forms.notifications import NotificationForm
from datetime import date
from .models import TeacherEvaluation
from forms.workbook import  WorkbookForm
# Create your views here.

#-------------------------------------生徒関係--------------------------------
@user_passes_test(lambda u: u.is_superuser)
@login_required
def student_list(request):
    students = Student.objects.all()

    search_query = request.GET.get('search', '')  # Get search query from request
    
    if search_query:
        students = students.filter(student_name__icontains=search_query)

    context = {
        "students":students,
        'search_query': search_query,
    }

    return render(request, 'dashboard/student_list.html',context)

@user_passes_test(lambda u: u.is_superuser)
@login_required
def student_detail(request, pk):
    student = Student.objects.get(pk=pk)
    return render(request, 'dashboard/student_detail.html', {'student': student})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def student_create(request):
    # フォームを作成してPOSTされた場合の処理
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.parent = request.user
            student.save()
            return redirect('dashboard:student_list',)
    # GETリクエストの場合はフォームを表示する
    else:
        form = StudentForm()
    return render(request, 'dashboard/create_student.html', {'form': form})

#---------------------------------------------------------------------------------


#-------------------------------------月謝を管理する--------------------------------

#塾生の月謝
@user_passes_test(lambda u: u.is_superuser)
@login_required
def tuition_list(request):
    students = Student.objects.all()
    tuitions = Tuition.objects.all().order_by('due_date')
    ticket_list ={}
    for tuition in tuitions:
        tickets = tuition.tickets.all()
        total_ticket = 0
        ticket_sum = 0
        
        for ticket in tickets:
            total_ticket += ticket.price
            #チケットの合計枚数を格納する変数
            ticket_sum += int(ticket.ticket_type)
            tuition.ticket_num = ticket_sum
            #月謝+チケット代
            tuition.amount = total_ticket + tuition.amount
        
        ticket_list[tuition.student.id] = tickets
    ticket_list = ticket_list.items()

    search_query = request.GET.get('search', '')  # Get search query from request
    
    if search_query:
        tuitions = tuitions.filter(student__student_name__icontains=search_query)

    context = {
        'tuitions': tuitions,
        "students":students,
        'ticket_list': ticket_list,
        'search_query': search_query,
    }

    return render(request, 'dashboard/tuition_list.html', context)

#塾外生の月謝
@user_passes_test(lambda u: u.is_superuser)
@login_required
def E_tuition_list(request):
    tuitions = External_Tuition.objects.all().order_by('due_date')
    ticket_list ={}
    for tuition in tuitions:
        tickets = tuition.tickets.all()
        total_ticket = 0
        ticket_sum = 0
        
        for ticket in tickets:
            total_ticket += ticket.price
            #チケットの合計枚数を格納する変数
            ticket_sum += int(ticket.ticket_type)
            tuition.ticket_num = ticket_sum
            #授業料の確定
            tuition.amount = total_ticket
    
    ticket_list[tuition.student.id] = tickets
    ticket_list = ticket_list.items()
    search_query = request.GET.get('search', '')  # Get search query from request
    
    if search_query:
        tuitions = tuitions.filter(student__student_name__icontains=search_query)

    context = {
        'tuitions': tuitions,
        'ticket_list': ticket_list,
        'search_query': search_query,
        'ticket_sum':ticket_sum,
    }

    return render(request, 'dashboard/E_tuition_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
@login_required
def tuition_detail(request, pk):
    tuition = Tuition.objects.get(pk=pk)
    return render(request, 'dashboard/tuition_detail.html', {'tuition': tuition})

#---------------------------------------------------------------------------------

#-------------------------------------売り上げ管理--------------------------------
@user_passes_test(lambda u: u.is_superuser)
@login_required
def caluculate(request):
    total_sales = []
  
    for i in range(1, 13):
        if i == 2:
            d = calendar.monthrange(2023, i)[1]
        elif i in [4, 6, 9, 11]:
            d = 30
        else:
            d = 31
        start_date = datetime(2023, i, 1)
        end_date = datetime(2023, i, d)
        total_calculate = Payment.objects.filter(payment_status='済み', payment_date__gte=start_date, payment_date__lte=end_date).aggregate(total_sales=Sum('amount'))['total_sales'] or 0
        total_sales.append(total_calculate)
    annual = sum(total_sales)
    return render(request, 'sales/monthly_sales.html', {'total_sales': total_sales,"annual":annual})




#---------------------------------------------------------------------------------


#-------------------------------------プロジェクト管理--------------------------------
@user_passes_test(lambda u: u.is_superuser)
@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'dashboard/project_list.html', {'projects': projects})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard:project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'dashboard/project_edit.html', {'form': form})


#---------------------------------------------------------------------------------
#日報


    
#--------------------講師関係----------------------

@user_passes_test(lambda u: u.is_superuser)
@login_required
#講師登録
def instructor_create(request):
    form = InstructorRegistrationForm()
    if request.method == 'POST':
        form = InstructorRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            gender = form.cleaned_data['gender']
            birth_date = form.cleaned_data['birth_date']
            instructor = Instructor(name=name,gender=gender, birth_date=birth_date, password='20210927')
            instructor.save()
            return redirect('dashboard:instructor_list')
    return render(request, 'dashboard/create_instructor.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
@login_required
#講師リスト
def instructor_list(request):
    instructors = Instructor.objects.all()

    search_query = request.GET.get('search', '')  # Get search query from request
    
    if search_query:
        instructors = instructors.filter(name__icontains=search_query)

    context = {
        'instructors': instructors,
        'search_query': search_query,
    }

    return render(request, 'dashboard/instructor_list.html',context)


def instructor_detail(request, pk):
    instructor = Instructor.objects.get(pk=pk)
    return render(request, 'dashboard/instructor_detail.html', {'instructor': instructor})


#-------------------------------------------授業予約---------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
@login_required
def reservation_list_view(request):
    reservations = Reservation.objects.all().order_by("time","reserved_time")

    search_query = request.GET.get('search', '')  # Get search query from request
    
    if search_query:
        reservations = reservations.filter(reserved_time__icontains=search_query)

    context = {
        'reservations': reservations,
        'search_query': search_query,
    }


    return render(request, 'dashboard/reservation_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
@login_required
def todays_lesson_view(request):
    today = date.today()
    start_time = datetime.combine(today, datetime.min.time())
    end_time = datetime.combine(today, datetime.max.time())

    todays_lesson = Reservation.objects.filter(reserved_time__range=(start_time, end_time)).order_by('time')

    return render(request, 'dashboard/todays_lesson.html', {'todays_lesson': todays_lesson})


#----------------------お問い合わせの確認----------------------
@user_passes_test(lambda u: u.is_superuser)
@login_required
def contact_list(request):
    contacts = Contact.objects.all()

    search_query = request.GET.get('search', '')  # Get search query from request
    
    if search_query:
        contacts = contacts.filter(name__icontains=search_query)

    context = {
        'contacts': contacts,
        'search_query': search_query,
    }
    return render(request, 'dashboard/contact_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
@login_required
def contact_detail(request,pk):
    contact = get_object_or_404(Contact, pk=pk)
    context = {
        'contact': contact
    }
    return render(request, 'dashboard/contact_detail.html', context)

#-------------------------お知らせ配信----------------------------
@user_passes_test(lambda u: u.is_superuser)
@login_required
def create_notifications(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save()
            recipients = form.cleaned_data['recipients']
            notification.recipients.set(recipients)
            return redirect('dashboard:student_list')
    else:
        form = NotificationForm()
    
    return render(request, 'dashboard/notification_create.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def send_notification_to_all_users(title, content):
    recipients = User.objects.all()
    notification = Notification.objects.create(title=title, content=content)
    notification.recipients.set(recipients)


#--------------------アンケート結果-----------------
@user_passes_test(lambda u: u.is_superuser)
@login_required
def questionnaire_answer(request):
    questionnaires  =  TeacherEvaluation.objects.all()

    search_query = request.GET.get('search', '')  # Get search query from request
    
    if search_query:
        questionnaires = questionnaires.filter(instructor__name__icontains=search_query)

    context = {
        'questionnaires':questionnaires,
        'search_query': search_query,
    }

    return render(request, 'dashboard/questionnaire.html' ,context)


#--------------------教材登録-----------------------
@user_passes_test(lambda u: u.is_superuser)
@login_required
def add_workbook(request):
    if request.method == 'POST':
        form = WorkbookForm(request.POST, request.FILES)
        if form.is_valid():
            workbook = form.save()
            return redirect('dashboard:student_list')
    else:
        form = WorkbookForm()
    return render(request, 'dashboard/workbook.html', {'form': form})