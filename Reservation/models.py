from django.db import models
from django.utils import timezone
from Instructor.models import Schedule,TimeSlot
from Student.models import Student


#講師スケジュール

#全体の予約管理
class Reservation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,verbose_name ="生徒",null =True,)
    reserved_time = models.DateField(verbose_name ="予約時間")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name="スケジュール", null=True)
    time = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name="時間帯", null=True)


    class Meta:
        verbose_name = '全体予約'
        verbose_name_plural =  '全体予約'

    def __str__(self):
        return f'{self.student}'

class Report(models.Model):
    evaluate =(
        ("A","A"),
        ("B","B"),
        ("C","C"),
        ("D","D"),
        ("E","E"),
    )
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE,related_name='report')
    goal = models.CharField(max_length=255, verbose_name="授業の目標")
    achievement = models.CharField(max_length=255,choices=evaluate, verbose_name="達成度")
    comment = models.TextField(verbose_name="コメント")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '日報'
        verbose_name_plural = '日報'

    def __str__(self):
        return f'日報 - {self.reservation.student}'
    