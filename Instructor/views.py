from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Instructor,Schedule,Salary
from Reservation.models import Reservation,Report
from django.utils import timezone
from datetime import datetime,timedelta
from Student.models import Student
from forms.available import ScheduleForm
from datetime import date
from django.http import HttpResponseForbidden

#--------------------------------講師用---------------------------------


#ログイン後の処理
class index(LoginRequiredMixin,TemplateView):
    template_name ="instructor/index.html"
    model =Instructor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #userモデルにある講師とInstructorにある講師の一致（ログインできるようにするため）
        user = self.request.user
        instructor = Instructor.objects.get(user=user)
        context["instructor"] = instructor
        return context

#-----------------------------------------------授業関連-------------------------------------------------

#本日の授業
class Todaysclass(LoginRequiredMixin,TemplateView):
    template_name = 'instructor/todaysclass.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        instructor = Instructor.objects.get(user=user)
        #自分のシフトを全て取得
        my_schedules = Schedule.objects.filter(instructor_name=instructor)
        #シフトのidを取り出す
        schedule_ids = [schedule.id for schedule in my_schedules]
        #自分のシフトに入った予約を取得
        reservations = Reservation.objects.filter(schedule_id__in=schedule_ids)
        print(reservations)
        today = date.today()
        start_time = datetime.combine(today, datetime.min.time())
        end_time = datetime.combine(today, datetime.max.time())
        todayclasses = reservations.filter(reserved_time__range=(start_time, end_time)).order_by('time')
        print(todayclasses)
        students = Student.objects.filter(reservation__in=todayclasses)
        context["todayclasses"] = todayclasses
        context["students"] = students
        context["instructor"] = instructor
        return context


#授業履歴
@ login_required
def History_class(request,pk):
    me  = get_object_or_404(Instructor, pk=pk)

    #アクセス権チェック
    if request.user.pk != me.user.pk:
        return render(request, 'denied.html')  # アクセス拒否
    
    schedules = Schedule.objects.all()
    all_reservations = Reservation.objects.all()
    students = Student.objects.all()

    search_query = request.GET.get('search', '')
    search_date = request.GET.get('date', '')

    if search_query:
        all_reservations = all_reservations.filter(student__student_name__icontains=search_query)
    if search_date:
        try:
            search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
            tuitions = tuitions.filter(due_date=search_date)
        except ValueError:
            pass  # 例外処理: 日付が無効な形式の場合は何もしない
    
    context={
        "instructor":me,
        'search_query': search_query,
        "search_date":search_date,
        "schedules":schedules,
        "allreservation":all_reservations,
    }

    return render(request, 'instructor/history_class.html', context)




#-------------------------------------------シフト関連--------------------------------------------------
#シフト用カレンダー生成
@login_required
def create_available(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)

    if request.user.pk != instructor.user.pk:
        return render(request, 'denied.html')  # アクセス拒否

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            print(request.POST)
            schedule = form.save(commit=False)
            schedule.instructor_name = instructor
            schedule.save()
            form.save_m2m() 
            # 成功時の処理を追加する場合はここに記述してください
            return redirect('instructor:index')  # 成功時のリダイレクト先を設定
    else:
        initial_data = {'instructor_name': instructor}  # フォームの初期データとしてインストラクターを指定
        form = ScheduleForm(initial=initial_data)
    
    
    return render(request, 'instructor/available.html', {'form': form,'instructor':instructor})

#---------------------------------------------給料計算----------------------------------------------

@login_required
def sarary(request,pk):
    instructor = Instructor.objects.get(pk=pk)
    if request.user.pk != instructor.user.pk:
         return render(request, 'denied.html')  # アクセス拒否
    
    salaries = Salary.objects.filter(instructor_id=pk) 
    #給与計算がされていたら
    if salaries:
        current_month = datetime.now().month
        #過去の給与を取得して一つずつチェック
        for salary in salaries:
            #ManytoManyのフィールドの取り出し方（QuerySet）
            salary_month = salary.monthly_salaries.values_list('month', flat=True)
            #QuerySet（list）から値を取り出す
            confirm_month = salary_month[0]
            #給与の月と先月が一緒だったら
            if confirm_month == current_month - 1: 
                #ManytoManyのフィールドの取り出し方（QuerySet）
                monthly_salary = salary.monthly_salaries.values_list("amount", flat=True)
                #QuerySet（list）から値を取り出す
    confirm_monthly_salary =monthly_salary[0]
                


    context={
        "instructor":instructor,
        "monthly_salary":confirm_monthly_salary,
        "current_month":current_month,

    }
    return render(request, 'instructor/sarary.html',context)


#---------------------------------------------本部からの通知----------------------------------------------
