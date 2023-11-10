from django.db import models
import datetime
from User.models import User
from django.urls import reverse
from datetime import date, timedelta
from Instructor.models import Instructor
# Create your models here.

#生徒
class Student(models.Model):
    grades = (
        ('1年', '1年'),
        ('2年', '2年'),
        ('3年', '3年'),
        ('4年', '4年'),
        ('5年', '5年'),
        ('6年', '6年'),
    )
    genders = (
        ('男', '男'),
        ('女', '女'),
    )
    classrooms =(
        ("中学受験対策コース","中学受験対策コース"),
        ("高校受験対策コース","高校受験対策コース"),
        ("大学受験対策コース","大学受験対策コース"),
        ("基礎学力集中コース","基礎学力集中コース"),
        ("オーダーメイドコース","オーダーメイドコース"),
        ("パッケージプラン","パッケージプラン"),
    )
    plan = (
        ("フリープラン","フリープラン"),
        ("マンツーマン","マンツーマン"),
    )
    subjects = (
        ("数学","数学"),
        ("英語","英語"),
    )
    student_name = models.CharField(max_length =15,default=None,verbose_name="生徒名")
    first_name = models.CharField(max_length=50,verbose_name="ふりがな（性）",blank = True, null = True) #生徒の苗字
    last_name = models.CharField(max_length=50, verbose_name="ふりがな（名）",blank =True,null = True) #生徒の名前
    gender = models.CharField(max_length=10,choices = genders,verbose_name="性別") #生徒の性別
    parent = models.ForeignKey(User, default = 0, on_delete=models.CASCADE, related_name = "students",verbose_name="保護者")
    birth_date = models.DateField(verbose_name="生年月日",blank = True)
    grade = models.CharField(max_length =10,default = None,choices = grades,verbose_name="学年")
    classroom = models.CharField(max_length=10,choices = classrooms,verbose_name="クラス",blank =True) 
    plan = models.CharField(max_length=10,choices = plan,verbose_name="プラン",blank =True) 
    subjects  = models.CharField(max_length=10,choices = subjects,verbose_name="教科",blank =True) 
    to_1 = models.BooleanField(default=False, verbose_name="マンツーマン")
    to_2 = models.BooleanField(default=False, verbose_name="1対2")
    is_external = models.BooleanField(default=False, verbose_name="塾外生")
    
    def get_absolute_url(self):
        return reverse('my_page', args=[str(self.pk)])
    
    @property
    def age(self):
        today = datetime.date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age


    def __str__(self):
        return self.student_name
    
    class Meta:
        verbose_name = '生徒'
        verbose_name_plural = '生徒一覧'



#プロジェクト
class Project(models.Model):
    members = models.ManyToManyField(Student,blank =True,verbose_name="プロジェクトメンバー")
    name = models.CharField(max_length=100,verbose_name="プロジェクト名")
    description = models.TextField(verbose_name="プロジェクトの説明")
    start_date = models.DateField(verbose_name="開始日")
    end_date = models.DateField(verbose_name="終了日")
    status = models.CharField(max_length=20, choices=(
        ('ongoing', '進行中'),
        ('finished', '完了'),
        ('cancelled', '中止'),
    ),verbose_name="ステータス")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'プロジェクト'
        verbose_name_plural = 'プロジェクト一覧'


#入退室
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    checkin_time = models.DateTimeField(null=True, blank=True)
    checkout_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = '入退室'
        verbose_name_plural = '入退室一覧'


#---------------チケット管理-----------------------
class Ticket(models.Model):
    TICKET_CHOICES = (
        ('1', '1枚購入 (3500円)'),
        ('4', '4枚購入 (14000円)'),
        ('8', '8枚購入 (24500円)'),
    )

    ticket_type = models.CharField(max_length=2, choices=TICKET_CHOICES, verbose_name="回数券の種類")
    purchase_date = models.DateField(auto_now_add=True, verbose_name="購入日")
    valid_until = models.DateField(verbose_name="有効期限")
    usage_count = models.PositiveIntegerField(default=0, verbose_name="使用回数")
    remaining_count = models.PositiveIntegerField(default=0,verbose_name="残りの枚数")
    price = models.PositiveIntegerField(verbose_name="価格")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="生徒")

    class Meta:
        verbose_name = "回数券"
        verbose_name_plural = "回数券"

    def __str__(self):
        return f"{self.ticket_type} ({self.price}円)"
    
    def add_tickets(self, ticket_type):
        if ticket_type == '1':
            self.remaining_count += 1
            self.price =3500
        elif ticket_type == '4':
            self.remaining_count += 4
            self.price =14000
        elif ticket_type == '8':
            self.remaining_count += 8
            self.price =24500
        self.save()

    def save(self, *args, **kwargs):
        # 有効期限を購入日から1年に設定
        self.valid_until = self.purchase_date + timedelta(days=365)
        super().save(*args, **kwargs)


#---------------支払い管理-----------------------
#継続的な支払いの処理
class Tuition(models.Model):
    AGE_GROUP_CHOICES = (
        ('小学生', '小学生'),
        ('中学生', '中学生'),
        ('高校生', '高校生'),
    )

    CLASS_COUNT_CHOICES = (
        (1, '週1回'),
        (2, '週2回'),
    )

    payment_statuses = (
        ('未払い', '未払い'),
        ('済み', '済み'),
        ('調整中', '調整中'),
        ('払い戻し済み', '払い戻し済み'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tuitions', verbose_name='生徒')
    payment_date = models.DateField(verbose_name="支払い日",blank=True, null=True)
    amount = models.IntegerField(verbose_name="金額",blank=True, null=True)
    payment_status = models.CharField(max_length=10, choices=payment_statuses, verbose_name="支払い状況", default="未払い")
    due_date = models.DateField(verbose_name="支払い期限", null=True, blank=True)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES, verbose_name="年齢グループ", blank=True, null=True)
    class_count = models.IntegerField(choices=CLASS_COUNT_CHOICES, verbose_name="週の回数",default = 1)
    tickets = models.ManyToManyField(Ticket, verbose_name="チケットの金額")
    ticket_num = models.IntegerField(verbose_name="チケットの購入枚数",blank=True, null=True,default=0)
    

     #継続的な支払いの処理
    def save(self, *args, **kwargs):
        if self.payment_status == '済み':
            #次の支払期日の設定
            current_due_date = self.due_date
            next_due_date = current_due_date.replace(day=15)
            if current_due_date.day >= 15:
                next_due_date = next_due_date.replace(month=next_due_date.month + 1)

            tickets = self.tickets.all()
            total_ticket = 0
            for ticket in tickets:
                total_ticket += ticket.price
            total_amount = total_ticket + self.amount

        # 新しいTuitionオブジェクトを作成して保存
            next_tuition = Tuition.objects.create(
                student=self.student,
                due_date=next_due_date,
                amount=self.amount,
                class_count=self.class_count,  
         )

        # 新しいPaymentオブジェクトを作成して保存
            
            payment = Payment.objects.create(
                student=self.student,
                due_date=self.due_date,
                payment_date=datetime.datetime.now().date(),
                amount=total_amount,
                payment_status = self.payment_status
            )
            #チケット料金の削除
            self.tickets.clear()

        #年齢に応じた料金設定
        age = self.student.age
        class_count = self.class_count

        if age < 13:
            age_group = '小学生'
            self.age_group = '小学生'
        elif age < 16:
            age_group = '中学生'
            self.age_group = '中学生'
        else:
            age_group = '高校生'
            self.age_group = '高校生'

         #講師1名-生徒2名の場合(小学生)
        if age_group=="小学生" and class_count == 1 and self.student.to_2 == True:
            self.amount = 7500
        elif age_group=="小学生" and class_count == 2 and  self.student.to_2 == True:
            self.amount = 15000
        #講師1名-生徒1名の場合(小学生)
        if age_group=="小学生" and class_count == 1 and self.student.to_1 == True:
            self.amount = 10700
        elif age_group=="小学生" and class_count == 2 and  self.student.to_1 == True:
            self.amount = 21400

        #講師1名-生徒2名の場合(中学生)
        if age_group=="中学生" and class_count == 1 and self.student.to_2 == True:
            self.amount = 11000
        elif age_group=="中学生" and class_count == 2 and self.student.to_2 == True:
            self.amount = 22000
        #講師1名-生徒1名の場合(中学生)
        if age_group=="中学生" and class_count == 1 and self.student.to_1 == True:
            self.amount = 15000
        elif age_group=="中学生" and class_count == 2 and self.student.to_1 == True:
            self.amount = 30000
        
        #講師1名-生徒1名の場合(高校生)
        if age_group=="高校生" and class_count == 1 and self.student.to_1 == True:
            self.amount = 17000
        elif age_group=="高校生" and class_count == 2 and  self.student.to_1 == True:
            self.amount = 34000
        
        # 支払い期限を生成
        if not self.due_date:
            today = datetime.date.today()
            #もし今日(支払日)が15日より大きかったら
            if today.day >= 15:
                #翌月の15に支払日を設定
                due_date = datetime.date(today.year, today.month + 1, 15)
                #もし今日(支払日)が25日未満だったら
            else:
                #今月の15日に設定
                due_date = datetime.date(today.year, today.month, 15)
            self.due_date = due_date

        super().save(*args, **kwargs)

        if self.payment_status == '済み':
            self.delete()
    
    class Meta:
        verbose_name = '月謝'
        verbose_name_plural = '月謝管理'

    def __str__(self):
        return f"{self.student.student_name}({self.student.pk}): {self.amount}円"


#塾外生の単発的な授業料
class External_Tuition(models.Model):

    AGE_GROUP_CHOICES = (
        ('小学生', '小学生'),
        ('中学生', '中学生'),
        ('高校生', '高校生'),
    )

    payment_statuses = (
        ('未払い', '未払い'),
        ('済み', '済み'),
        ('調整中', '調整中'),
        ('払い戻し済み', '払い戻し済み'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='external_tuition', verbose_name='生徒')
    payment_date = models.DateField(verbose_name="支払い日",blank=True, null=True)
    amount = models.IntegerField(verbose_name="金額",blank=True, null=True,default=0)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES, verbose_name="年齢グループ", blank=True, null=True)
    payment_status = models.CharField(max_length=10, choices=payment_statuses, verbose_name="支払い状況", default="未払い")
    due_date = models.DateField(verbose_name="支払い期限", null=True, blank=True)
    tickets = models.ManyToManyField(Ticket, verbose_name="チケットの金額")
    ticket_num = models.IntegerField(verbose_name="チケットの購入枚数",blank=True, null=True,default=0)

    def __str__(self):
        return f"{self.student}"
    
    class Meta:
        verbose_name = '塾外生月謝'
        verbose_name_plural = '塾外生月謝'

    
    def save(self, *args, **kwargs):
        if self.payment_status == '済み':
            #次の支払期日の設定
            current_due_date = self.due_date
            next_due_date = current_due_date.replace(day=25)
            if current_due_date.day > 15:
                next_due_date = next_due_date.replace(month=next_due_date.month + 1)

            tickets = self.tickets.all()
            total_ticket = 0
            for ticket in tickets:
                total_ticket += ticket.price
            total_amount = total_ticket 
        
        age = self.student.age
        if age < 13:
            age_group = '小学生'
            self.age_group = '小学生'
        elif age < 16:
            age_group = '中学生'
            self.age_group = '中学生'
        else:
            age_group = '高校生'
            self.age_group = '高校生'

        # 新しいTuitionオブジェクトを作成して保存
            next_tuition = External_Tuition.objects.create(
                student=self.student,
                due_date=next_due_date,
                amount=self.amount,
                

         )

        # 新しいPaymentオブジェクトを作成して保存
            
            payment = Payment.objects.create(
                student=self.student,
                due_date=self.due_date,
                payment_date=datetime.datetime.now().date(),
                amount=total_amount,
                payment_status = self.payment_status
            )
            #チケット料金の削除
            self.tickets.clear()
         # 支払い期限を生成
        if not self.due_date:
            today = datetime.date.today()
            #もし今日(支払日)が15日より大きかったら
            if today.day > 15:
                #翌月の15に支払日を設定
                due_date = datetime.date(today.year, today.month + 1, 15)
                #もし今日(支払日)が15日未満だったら
            else:
                #今月の15日に設定
                due_date = datetime.date(today.year, today.month, 15)
            self.due_date = due_date

        super().save(*args, **kwargs)

        if self.payment_status == '済み':
            self.delete()


#支払い済みのレコード
class Payment(models.Model):

    payment_statuses = (
        ('未払い', '未払い'),
        ('済み', '済み'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=10,choices=payment_statuses,verbose_name="支払い状況", default="未払い")
    due_date = models.DateField(verbose_name="期限",blank=True,null =True)
    payment_date = models.DateField(verbose_name="支払日")
    amount = models.IntegerField(verbose_name="金額")   

    class Meta:
        verbose_name = '支払い履歴'
        verbose_name_plural = '支払い履歴'


#---------------欠席管理-----------------------
#欠席と振替日
class Absence(models.Model):
    reasons = (
        ('病気', '病気'),
        ('家庭の事情', '家庭の事情'),
        ('その他', 'その他'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="生徒")
    date = models.DateField(verbose_name="欠席日")
    reason = models.CharField(max_length=20, choices=reasons, verbose_name="欠席理由")
    request_date = models.DateTimeField(auto_now_add=True, verbose_name="申請日時")
    substitute_date = models.DateField(verbose_name="振り替え日", blank=True, null=True)
    is_approved = models.BooleanField(default=False, verbose_name="承認済みかどうか")

    class Meta:
        verbose_name = "欠席"
        verbose_name_plural = "欠席"

