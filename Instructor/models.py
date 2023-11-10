from django.db import models
import datetime
# Create your models here.
from User.models import User


class Instructor(models.Model):
    genders=(
        ("男","男"),
        ("女","女"),
    )
    name = models.CharField(max_length =15,default=None,verbose_name="講師名",null =True)
    is_teacher = models.BooleanField(default=True, verbose_name="講師フラグ")
    user=models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    birth_date = models.DateField(verbose_name="生年月日",blank = True,null =True)
    like = models.CharField(max_length=30, verbose_name="好きな食べ物",blank = True,null =True)
    gender =models.CharField(max_length=2,choices=genders,verbose_name="性別",blank = True,null =True)
    photo = models.ImageField(upload_to='instructor_photos', verbose_name="写真", blank=True, null=True)
    online_support = models.BooleanField(default=False, verbose_name="オンライン対応")
    in_person_support = models.BooleanField(default=False, verbose_name="対面での対応")
    sarary = models.IntegerField(verbose_name="コマ給",default=1200)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '講師'
        verbose_name_plural = '講師一覧'

    @property
    def age(self):
        today = datetime.date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age
    
class Salary(models.Model):
    instructor = models.OneToOneField(Instructor, on_delete=models.CASCADE, verbose_name="講師")
    monthly_salaries = models.ManyToManyField('MonthlySalary', verbose_name="月間給与")
    annual_salaries = models.ManyToManyField('AnnualSalary', verbose_name="年間給与", blank=True)

    class Meta:
        verbose_name = '給与'
        verbose_name_plural = '給与一覧'

    def __str__(self):
        return str(self.instructor)

class MonthlySalary(models.Model):
    koma = models.IntegerField(verbose_name="コマ数",default=0)
    month = models.IntegerField(verbose_name="給与の月", null=True, blank=True)
    amount = models.IntegerField(verbose_name="給与金額")

    def __str__(self):
        return f"{self.month}月 - {self.amount}"


class AnnualSalary(models.Model):
    year = models.IntegerField(verbose_name="給与の年")
    amount = models.IntegerField(verbose_name="給与金額")

    def __str__(self):
        return f"{self.year} - {self.amount}"


class TimeSlot(models.Model):
    times =(
        ("10:00~11:00","10:00~11:00"),
        ("11:10~12:10","11:10~12:10"),
        ("12:20~13:20","12:20~13:20"),
        ("13:30~14:30","13:30~14:30"),
        ("14:40~15:40","14:40~15:40"),
        ("15:50~16:50","15:50~16:50"),
        ("17:00~18:00","17:00~18:00"),
        ("18:10~19:10","18:10~19:10"),
        ("19:20~20:20","19:20~20:20"),
        ("20:30~21:30","20:30~21:30"),
    )
    time = models.CharField(max_length=50,choices=times,verbose_name="時間割") 

    class Meta:
        verbose_name = '時間割'
        verbose_name_plural = '時間割'

    def __str__(self):
        return self.time
    
class Schedule(models.Model):
    date = models.DateField(verbose_name="日付",null =True) 
    time = models.ManyToManyField(TimeSlot,related_name="schedules")
    instructor_name = models.ForeignKey(Instructor, on_delete=models.CASCADE,null=True,verbose_name = "講師名")


    class Meta:
        verbose_name = '講師スケジュール'
        verbose_name_plural = '講師スケジュール'

    def __str__(self):
        return str(self.instructor_name)
    
 
