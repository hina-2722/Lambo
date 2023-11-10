# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from .models import Schedule,Reservation,Report,TimeSlot
from Instructor.models import Instructor
from django.utils import timezone
from Student.models import Student,Ticket
import datetime
from datetime import date
from calendar import monthrange
from django.utils import formats
from datetime import datetime
from django.contrib import messages
from django.db.models import Count
from forms.report import ReportForm
from datetime import date, timedelta
#-----------------------生徒が予約に必要な機能----------------------

#カレンダーで表示するビュー
def schedule_calendar(request, pk):
    student = get_object_or_404(Student, pk=pk)
    tomorrow = date.today() + timedelta(days=1)
    end_date = tomorrow + timedelta(days=27)

    calendar_data = []
    current_date = tomorrow
    while current_date <= end_date:
        day_data = {
            'date': current_date,
            'day_of_week': current_date.strftime("%A"),
            'has_schedule': Schedule.objects.filter(date=current_date).exists(),
        }
        calendar_data.append(day_data)
        current_date += timedelta(days=1)

    weeks_data = []
    week_data = []
    for day_data in calendar_data:
        week_data.append(day_data)
        if len(week_data) == 7:
            weeks_data.append(week_data)
            week_data = []

    if week_data:
        weeks_data.append(week_data)

    context = {
        'year': tomorrow.year,
        'month': tomorrow.month,
        'calendar_data': calendar_data,
        'student': student,
        'weeks_data': weeks_data,
    }

    return render(request, 'reservation/schedule_calendar.html', context)


#講師の選択
def schedule_detail(request, year, month, day, pk):
    student = get_object_or_404(Student, pk=pk)
    target_date = date(year, month, day)
    # 前ページで取得した日付と同じシフトを持つ講師の情報を取得
    schedules = Schedule.objects.filter(date=target_date).annotate(reservation_count=Count('reservation'))
    # 自分が既に予約した情報を取得
    reserved_schedules = list(student.reservation_set.all().values_list('schedule_id', flat=True))
    reserved_times = student.reservation_set.all().values_list('time_id', flat=True)
    available_times = {}
    for schedule in schedules:
        #スケジュールの時間割を全て格納
        time_slots = list(schedule.time.all())
        #全体の予約の中から選択したスケジュールのみをフィルタリング
        whole_reservation = Reservation.objects.filter(schedule_id = schedule.id)
        #全体予約の中からtime_idと、その数を数える
        time_count = whole_reservation.values('time_id').annotate(count=Count('time_id'))
        for duplicate in time_count:
            duplicate_count = duplicate["count"]
            kind_of_time = duplicate["time_id"]
            appear_time = TimeSlot.objects.get(id=kind_of_time)
            if duplicate_count == 3:
                time_slots.remove(appear_time)

        reserved_schedules = student.reservation_set.all().filter(schedule_id=schedule.id)
        #自分が予約をしているかの確認
        if reserved_schedules:
            for reserved_schedule in reserved_schedules:
                if reserved_schedule.time in time_slots:
                    time_slots.remove(reserved_schedule.time)
            available_times[schedule.pk] = [str(time_slot.time) for time_slot in time_slots]
    
    context = {
        'date': target_date,
        'schedules': schedules,
        'student': student,
        'reserved_schedules': reserved_schedules,
        'reserved_times': reserved_times,
        'available_times': available_times,
        "time_slots":time_slots,
    }
    return render(request, 'reservation/instructor_available.html', context)


#予約の最終確認
def create_reservation(request,pk):
    student = get_object_or_404(Student, pk=pk)
    schedule = get_object_or_404(Schedule, pk=request.POST.get('schedule_id'))
    tickets = Ticket.objects.filter(student=student).order_by('purchase_date')
    if request.method == 'POST':
        reserved_time_str = request.POST.get('reserved_time')
        reserved_time = datetime.strptime(reserved_time_str, '%Y年%m月%d日')
        formatted_reserved_time = formats.date_format(reserved_time, format='Y年m月d日')
        selected_time_slot = request.POST.get('selected_time_slot')
        context = {
            'student': student,
            'reserved_time': formatted_reserved_time,
            "schedule":schedule,
            "selected_time_slot":selected_time_slot,
            "tickets":tickets,
        }
        return render(request, 'reservation/reservation_confirm.html', context)
    
    # POSTメソッド以外の場合はエラーメッセージを表示し、予約選択画面にリダイレクトする
    else:
        return redirect('reservation:schedule_list', pk=pk)
    


#予約確定
def confirm_reservation(request, pk):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=pk)
        schedule_id = request.POST.get('schedule_id')
        reserved_time_str = request.POST.get('reserved_time')
        reserved_time = datetime.strptime(reserved_time_str, '%Y年%m月%d日').date() 
        schedule = get_object_or_404(Schedule, pk=schedule_id)

        # 関連付けられたManyToManyフィールドに選択された値を保存
        selected_time_slot_value = request.POST.get('time_slot')
        selected_time_slot = schedule.time.filter(time=selected_time_slot_value).first()

        if selected_time_slot:
            # チケットの有無を確認
            ticket = Ticket.objects.filter(student=student).order_by('purchase_date').first()
            if ticket.remaining_count > 0:
                # チケットがあり、残り枚数が1枚以上の場合
                # 予約情報を保存
                reservation = Reservation.objects.create(
                    student=student,
                    schedule=schedule,
                    reserved_time=reserved_time,
                    time=selected_time_slot
                )
                # チケットを消費する
                ticket.remaining_count -= 1
                ticket.usage_count += 1
                ticket.save()

                if ticket.remaining_count ==0:
                    # チケットを削除する
                    ticket.delete()

                # 予約完了後の処理を追加（例: マイページへのリダイレクトやメッセージの表示など）
                messages.success(request, '予約が確定しました')
                return redirect('student:mypage', pk=pk)
            else:
                # チケットがないか、残り枚数が0の場合
                messages.error(request, 'チケットがありません')

    # POSTメソッド以外の場合はエラーメッセージを表示し、予約選択画面にリダイレクトする
    else:
        messages.error(request, '予約の確定に失敗しました')
        return redirect('reservation:schedule_list', pk=pk)


#----------------------------日報-----------------------------------

#日報作成
def create_report(request, pk, reservation_pk):
    reservation = get_object_or_404(Reservation, pk=reservation_pk)
    instructor = get_object_or_404(Instructor, pk=pk)
    try:
        report = reservation.report
    except Report.DoesNotExist:
        report = None

    user_matches_instructor = instructor.pk == reservation.schedule.instructor_name.pk

    print(user_matches_instructor)
    if request.method == 'POST':
        form = ReportForm(request.POST,instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.reservation = reservation
            report.save()
            return redirect('instructor:todays_class',pk=instructor.pk)
    else:
        form = ReportForm(instance=report)
    context={
        'form': form, 
        'reservation': reservation,
        "instructor":instructor,
        "user_matches_instructor":user_matches_instructor,


    }
    
    return render(request, 'reservation/report_create.html', context)

def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'report/detail.html', {'report': report})

def update_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_detail', report_id=report.id)
    else:
        form = ReportForm(instance=report)
    
    return render(request, 'report/update.html', {'form': form, 'report': report})

def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == 'POST':
        report.delete()
        return redirect('report_list')
    
    return render(request, 'report/delete.html', {'report': report})

def report_list(request):
    reports = Report.objects.all()
    return render(request, 'report/list.html', {'reports': reports})
