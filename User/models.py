from django.db import models
from django.utils import timezone
import random
from django.contrib.auth.models import (
   BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy
# Create your models here.


class UserManager(BaseUserManager):
   def create_user(self, email, password=None, **extra_fields):
       if not email:
           raise ValueError('正しく入力してください') # エラーメッセージ
       while True:
           customer_id = str(random.randint(100000, 999999))
           if not User.objects.filter(customer_id=customer_id).exists():
               break
       user = self.model(
           email=self.normalize_email(email),
           customer_id=customer_id,
         **extra_fields,
       )
       user.set_password(password) # passwordを引数にとってパスワード設定
       user.customer_id = customer_id
       user.save(using=self._db) # データベースへユーザーを保存
       
       return user
   
   def create_superuser(self,email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    return self.create_user(email, password, **extra_fields)
   
#↓↓↓↓↓↓createsuperuserがうまくいかない時↓↓↓↓↓↓
# python manage.py shell
#from django.contrib.auth import get_user_model
#...: User = get_user_model()
#...: user = User.objects.get(customer_id='対象のID')

#In [2]: user.is_staff = True
#...: user.is_superuser = True
#...: user.save()



   
class User(AbstractBaseUser,PermissionsMixin):
    customer_id = models.CharField(max_length = 6 ,unique = True,verbose_name="ID")
    username = models.CharField(max_length = 15 ,unique = True,verbose_name="保護者名")
    email = models.CharField(max_length = 100 ,unique = True,verbose_name="メールアドレス")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField( default=timezone.now, verbose_name="登録日")
    parent_first_name = models.CharField(max_length=20, verbose_name="ふりがな（名字）", blank=True, null=True)
    parent_last_name = models.CharField(max_length=20, verbose_name="ふりがな（名前）", blank=True, null=True)
    parent_tel = models.CharField(max_length=12, verbose_name="緊急連絡先", blank=True, null=True)
    USERNAME_FIELD = 'customer_id'
    REQUIRED_FIELDS = ["username","email"] 
    is_teacher = models.BooleanField(default=False, verbose_name="講師フラグ")

    objects = UserManager()
   
    def get_absolute_url(self):
       return reverse_lazy('student:index')
    
    class Meta:
        verbose_name = '保護者'
        verbose_name_plural = '保護者一覧'
        
    def __str__(self):
        return self.username






class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=20)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name + " - " + self.email


class Notification(models.Model):
    title = models.CharField(max_length=255, verbose_name="件名")
    content = models.TextField(verbose_name="お知らせ内容")
    recipients = models.ManyToManyField(User, related_name='notifications',verbose_name="保護者")
    created_at = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)  # 新着フラグ

    def __str__(self):
        return self.title