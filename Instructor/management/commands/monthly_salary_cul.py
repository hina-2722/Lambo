from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from Instructor.models import MonthlySalary, Schedule,Instructor,Salary
from Reservation.models import Reservation


class Command(BaseCommand):
    help = "テストコマンド"

    def handle(self, *args, **options):
         # 現在の月を取得
        current_month = datetime.now().month

        #month（DateField）に格納するためにDate形式での前月を取得
        today = datetime.now()
        last_day = today - timedelta(days=today.day) 

        # 先月の月を計算
        last_month = current_month - 1 if current_month > 1 else 12  # 1月の場合、12月に設定

        # Instructorモデルのすべてのインスタンスを取得
        instructors = Instructor.objects.all()

        for instructor in instructors:
            # 先月の予約をフィルタリング
            # まず、instructorに対応するScheduleを取得
            instructor_schedules = Schedule.objects.filter(instructor_name=instructor)
            # instructor_schedules に対応するReservationを取得
            reservations = Reservation.objects.filter(schedule__in=instructor_schedules)
            last_month_reservations = []
            for reservation in reservations:
                if reservation.reserved_time.month == last_month:
                    last_month_reservations.append(reservation)
            #先月の予約の数をカウント
            reservation_count = len(last_month_reservations)
            #月の給与計算（Instructorのsararyとスケジュールの数を掛ける）
            calculated_salary = instructor.sarary * reservation_count
            #月間給与を保存
            monthly_salary = MonthlySalary.objects.create(koma =reservation_count, month=last_month, amount=calculated_salary)
            #Salaryモデルのインスタンスを取得
            salary_instance, created = Salary.objects.get_or_create(instructor=instructor)
            #月間給与を追加（ManyToManyフィールドにはset()メソッドを使用）
            salary_instance.monthly_salaries.set([monthly_salary])
            print(f'月間給与を保存しました: {reservation_count}{salary_instance.monthly_salaries}')

        