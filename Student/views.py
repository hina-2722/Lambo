from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import TemplateView
from .models import Student ,Attendance,Tuition,Payment,Ticket,External_Tuition
from User.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import qrcode
from io import BytesIO
import base64
from Reservation.models import Reservation,Report
from django.http import HttpResponseForbidden
from Instructor.models import Schedule,Instructor
from dashboard.models import Workbook
import datetime
from django.db.models import Sum
from datetime import date
from forms.questionnaire import TeacherEvaluationForm

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter,portrait
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# Create your views here.

    
class Mypage(LoginRequiredMixin,TemplateView):
    template_name ="index.html"
    model =Student

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student,pk=self.kwargs["pk"])
        tuition = Tuition.objects.filter(student=student)
        new_notifications = self.request.user.notifications.filter(is_new=True).order_by('-created_at')
        context["new_notifications"] = new_notifications

        # アクセス権のチェック
        if self.request.user != student.parent:
            return HttpResponseForbidden()  # アクセス拒否
        
        ticket_count = Ticket.objects.filter(student=student).aggregate(Sum('remaining_count'))['remaining_count__sum']
        context['ticket_count'] = ticket_count or 0
       
        context["student"] = student
        context["tuition"] = tuition
        context['digital_id_qrcode'] = mark_safe(self.generate_qrcode(student))
        return context
    
    def generate_qrcode(self, student):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(student.id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0) 
        return base64.b64encode(buffer.getvalue()).decode()
    
class Children(LoginRequiredMixin,TemplateView):
    template_name ="index_children_list.html"
    model =Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent = get_object_or_404(User, pk=self.request.user.id)
        students = Student.objects.filter(parent =parent)
       

        context["students"] = students
        return context
    
#入退室履歴
def attendance_history(request,pk):
    student = get_object_or_404(Student, pk=pk)
    attendance_list = Attendance.objects.filter(student=student).order_by('-checkin_time')

     # アクセス権のチェック
    if request.user != student.parent:
        return HttpResponseForbidden()  # アクセス拒否
    
    return render(request, 'student/attendance_history.html', {'attendance_list': attendance_list,"student":student})

#入室パンチ
def checkin(request,pk):
    # 生徒情報を取得する
    student = get_object_or_404(Student, pk=pk)

     # アクセス権のチェック
    if request.user != student.parent:
        return HttpResponseForbidden()  # アクセス拒否
    
    # リクエストがPOSTメソッドであるかチェックする
    if request.method == 'POST':
        # 生徒の出席情報を検索する
        attendance = Attendance.objects.filter(student=student, checkin_time__isnull=True).first()
        if attendance:
            # 出席情報が存在する場合は、チェックイン時刻を現在時刻に設定して保存する
            attendance.checkin_time = timezone.now()
            attendance.save()
            messages.success(request, '出席登録が完了しました')
        else:
            # 出席情報が存在しない場合は、新しい出席情報を作成して現在時刻を設定する
            attendance = Attendance.objects.create(student=student, checkin_time=timezone.now())
            messages.success(request, '出席登録が完了しました')
             # チェックイン後のページにリダイレクトする
        return HttpResponseRedirect(reverse('student:mypage', args=(student.pk,)))
    return render(request, 'index.html', {'student': student})

#退室パンチ
def checkout(request, pk):
    student = get_object_or_404(Student, pk=pk)

     # アクセス権のチェック
    if request.user != student.parent:
        return HttpResponseForbidden()  # アクセス拒否
    
    if request.method == 'POST':
        attendance = Attendance.objects.filter(student=student, checkout_time__isnull=True).first()
        if attendance:
            attendance.checkout_time = timezone.now()
            attendance.save()
            messages.success(request, '退室登録が完了しました')
        else:
            attendance = Attendance.objects.create(student=student, checkout_time=timezone.now())
            messages.success(request, '退室登録が完了しました')
        return redirect('student:mypage', pk=student.pk)
    return render(request, 'index.html', {'student': student})

#領収書生成
@login_required
def generate_receipt_pdf(request,pk):
    student = get_object_or_404(Student, pk=pk)
    payment = Payment.objects.filter(student=student).order_by('-payment_date').first()

    # アクセス権のチェック
    if request.user != student.parent:
        return HttpResponseForbidden()  # アクセス拒否

    if not payment:
        # 支払い情報が存在しない場合は何もしないか、エラー処理を行う
        return HttpResponse("支払い履歴がありません。")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{payment.id}.pdf"'

    tax = int(payment.amount*0.1)
    include_tax =int(payment.amount*1.1)

    #領収書のキャンバスを作る
    custom_width = 590  # カスタムページの幅（ポイント）
    custom_height = 380
    c = canvas.Canvas(response, pagesize=(custom_width, custom_height))
    #枠線
    c.rect(20, 20, 550, 350)
    # フォント登録
    NotoSans_MEDIUM_TTF = "./fonts/NotoSansJP-Medium.ttf"
    pdfmetrics.registerFont(TTFont('NotoSans', NotoSans_MEDIUM_TTF))
    font_size = 20
    c.setFont('NotoSans', font_size)
    # タイトル
    font_size = 24
    c.setFont('NotoSans', font_size)
    c.drawString(260, 335, '領  収  書')
   
    #宛先
    font_size = 18
    c.setFont('NotoSans', font_size)
    c.drawString(40, 290, f" {payment.student.parent}")
    c.drawString(280, 290, "様")
    #線
    c.line(30, 280, 350, 280)
    font_size = 9
    c.setFont('NotoSans', font_size)
    #但し書き
    c.drawString(110, 120, '但      授業料として')

    payment_date_formatted = payment.payment_date.strftime("%Y年%m月%d日")
    c.drawString(480, 290, f" {payment_date_formatted}")
    # 自社情報
    c.drawString(420, 80, '〒418-0022')
    c.drawString(420, 70, '静岡県富士宮市小泉1978-10')
    c.drawString(420, 60, 'INCITE')
    c.drawString(420, 50, '総合学習塾 アイミー')
    c.drawString(420, 40, '代表取締役社長  日向悠貴')
    # 合計金額
    font_size = 20
    c.setFont('NotoSans', font_size)
    c.drawString(60, 150, '合計金額')
    c.drawString(200, 150, f'¥{include_tax}')
    #線
    c.line(30, 140, 350, 140)

    # 小計、消費税、合計
    font_size = 9
    c.setFont('NotoSans', font_size)
    c.drawString(30, 80, '小計:')
    c.drawString(120, 80, f'¥{payment.amount}')
    c.line(30, 75, 180, 75)	

    c.drawString(30, 60, '消費税:(10%)')
    c.drawString(120, 60, f'¥{tax}')
    c.line(30, 55, 180, 55)	
    
    c.drawString(30, 40, '合計:')
    c.drawString(120, 40, f'¥{include_tax}')
    c.line(30, 35, 180, 35)



    c.save()

    return response

#月謝ステータス一覧
def tuition_list(request,pk):
    student = get_object_or_404(Student, pk=pk)

    # アクセス権のチェック
    child = get_object_or_404(Student,pk=pk)
    if request.user != child.parent:
        return HttpResponseForbidden()  # アクセス拒否

    if  student.is_external ==False:
            tuitions = Tuition.objects.get(student=student)
            tickets = tuitions.tickets.all()
            total_ticket = 0
            for ticket in tickets:
                total_ticket += ticket.price
            total_amount = total_ticket + tuitions.amount
    else:
            tuitions = External_Tuition.objects.get(student=student)
            tickets = tuitions.tickets.all()
            total_ticket = 0
            for ticket in tickets:
                total_ticket += ticket.price
            total_amount = total_ticket

    payment = Payment.objects.filter(student = student).order_by('-payment_date').first()
    context = {'student': student,  'tuitions': tuitions, 'payment': payment,"total_amount":total_amount,"total_ticket":total_ticket }

    return render(request, 'student/tuition_list.html', context)



#-------------------------------------日報確認---------------------------------
#日報
def report(request,pk):
    student = get_object_or_404(Student, pk=pk)
    
    # 生徒の予約情報を取得
    reservations = Reservation.objects.filter(student_id=student.id).order_by('reserved_time')
    instructors = Instructor.objects.filter(schedule__reservation__in=reservations).distinct()

    # アクセス権のチェック
    if request.user != student.parent:
        return HttpResponseForbidden()  # アクセス拒否
    
    context = {'student': student, "reservations":reservations,"instructors":instructors }
    return render(request, 'student/report.html', context)

#日報詳細
def report_detail(request,pk,report_id):
    student = get_object_or_404(Student, pk=pk)
    reservation = get_object_or_404(Reservation, id=report_id)

    # アクセス権のチェック
    if request.user != student.parent:
        return HttpResponseForbidden()  # アクセス拒否
    
    context = {'student': student, "reservation":reservation}
    return render(request, 'student/report_detail.html', context)


#予約確認
def student_reservation(request,pk):
    student = get_object_or_404(Student, pk=pk)  # 指定された pk の生徒を取得

     # アクセス権のチェック
    if request.user != student.parent:
        return HttpResponseForbidden()  # アクセス拒否
    
    #今日の日付を取得
    today_date = date.today() 
    # 生徒の予約情報を取得
    reservations = Reservation.objects.filter(student_id=student.id, reserved_time__gte=today_date).order_by('reserved_time', 'time__time')

#不具合等もなく、いらなかったら消してOK↓↓↓↓↓↓↓↓↓↓
# 予約情報を時間帯と講師でグループ化
    #grouped_reservations = groupby(reservations, key=lambda x: (x.reserved_time, x.schedule))
# グループごとに重複を削除して予約情報をリスト化
    #unique_reservations = []
    #for key, group in grouped_reservations:
       #unique_reservations.append(next(group))

     # スケジュールと講師情報を取得してコンテキストに追加
    schedules = Schedule.objects.filter(reservation__in=reservations)
    instructors = [schedule.instructor_name for schedule in schedules]
    selected_time = [ schedule.time for schedule in schedules]
    context = {
        'reservations': reservations,
        'student': student,
        'schedules': schedules,
        'instructors': instructors,
        "selected_time":selected_time,
    }
    return render(request, 'student/reservation.html', context)


#-----------------------------特典------------------------------
def benefit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    report_count = Report.objects.filter(reservation__student=student).count()
    # アクセス権のチェック
    if request.user != student.parent:
            return HttpResponseForbidden()  # アクセス拒否
    context = {
        'student': student,
        'report_count': report_count,
    }
    return render(request, 'student/benefit.html', context)


#---------------------チケット購入-------------------------------
def TicketPurchaseView(request,pk):
    student = get_object_or_404(Student, pk=pk)  # 指定された pk の生徒を取得

    # アクセス権のチェック
    if request.user != student.parent:
            return HttpResponseForbidden()  # アクセス拒否

    context = {
        'student': student,
    }
    #塾生の処理
    if request.method == 'POST':
        if student.is_external == False:
            ticket_type = request.POST.get('ticket_type')
            if ticket_type == "1":
                price = 3500
            elif ticket_type == "4":
                price = 14000
            elif ticket_type == "8":
                price =24500
            else:
                price=0
            ticket = Ticket.objects.create(student=student, ticket_type=ticket_type,price =price, purchase_date=datetime.date.today())
            ticket.add_tickets(ticket_type)
            tuition = Tuition.objects.filter(student=student).latest('id')
            tuition.tickets.add(ticket)  # チケットオブジェクトを追加
        #塾外生の処理
        else:
            ticket_type = request.POST.get('ticket_type')
            if ticket_type == "1":
                price = 3500
            elif ticket_type == "4":
                price = 14000
            elif ticket_type == "8":
                price =24500
            else:
                price=0
            ticket = Ticket.objects.create(student=student, ticket_type=ticket_type,price =price, purchase_date=datetime.date.today())
            ticket.add_tickets(ticket_type)
            tuition =External_Tuition.objects.filter(student=student).latest('id')
            tuition.tickets.add(ticket)

        messages.success(request, '購入が完了しました')
        return redirect('student:mypage', pk=pk)

    else:
        return render(request, 'student/ticket_purchase.html',context)
    
#---------------------教材---------------------

def workbook_list(request, pk):
    student = get_object_or_404(Student, pk=pk)

    workbooks = Workbook.objects.filter(student=student)

    # アクセス権のチェック
    if request.user != student.parent:
            return HttpResponseForbidden()  # アクセス拒否

    context = {
        'workbooks': workbooks,
        'student': student,
    }
    return render(request, 'student/workbook_list.html', context)

#----------------アンケート-------------

def teacher_evaluation_form(request,pk):
    student = get_object_or_404(Student, pk=pk)
    current_month = date.today().month

    # アクセス権のチェック
    if request.user != student.parent:
            return HttpResponseForbidden()  # アクセス拒否
    
    if request.method == 'POST':
        form = TeacherEvaluationForm(request.POST)
        if form.is_valid():
            teacher_evaluation = form.save(commit=False)
            teacher_evaluation.student = student  # ログインユーザーのIDを格納
            if current_month == 6:
                teacher_evaluation.title = "6月の講師アンケート"
            elif current_month == 12:
                 teacher_evaluation.title = "12月の講師アンケート"
            teacher_evaluation.save()
            form.save()
            messages.success(request, 'アンケートを送信しました')
            return redirect('student:mypage', pk=pk)
    else:
        form = TeacherEvaluationForm()

    context = {
        'form':form,
        'student': student,
    }

    return render(request, 'student/questionnaire.html', context)
