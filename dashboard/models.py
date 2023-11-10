from django.db import models
from Student.models import Student
from Instructor.models import Instructor


#-----------教材-------------
class Workbook(models.Model):
    name = models.CharField(max_length=255,verbose_name ="教材の名前")
    price = models.DecimalField(max_digits=8, decimal_places=2,verbose_name ="価格")
    image = models.ImageField(upload_to='materials',verbose_name ="画像")
    purchase_link = models.URLField(verbose_name ="購入リンク")
    level = models.CharField(max_length=100,verbose_name ="レベル")
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '教材'
        verbose_name_plural = '教材一覧'

#--------------アンケート---------------
class TeacherEvaluation(models.Model):
    title = models.CharField(max_length=30,verbose_name ="アンケート名",null =True,blank =True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE ,verbose_name ="生徒ID" ,null =True, blank =True)
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE,verbose_name ="講師名")
    instructor_rating = models.PositiveIntegerField(verbose_name='講師の評価', default=3)
    curriculum_rating = models.PositiveIntegerField(verbose_name='コース内容とカリキュラムの評価', default=3)
    satisfaction_rating = models.PositiveIntegerField(verbose_name='授業の満足度の評価', default=3)
    comment = models.TextField(verbose_name='その他のコメントや意見', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="回答日")

    class Meta:
        verbose_name = 'アンケート'
        verbose_name_plural = 'アンケート一覧'