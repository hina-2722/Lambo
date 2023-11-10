from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib import messages 
import random
from django.urls import reverse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from forms.signup import SignupForm
from forms.login import LoginForm
from .models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from forms.contact import ContactForm
from .models import Contact
from Student.models import Student
from .models import Notification
#講師用
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# Create your views here.


class UserLoginView(LoginView):  # 追加
   
   template_name = 'user/login.html'
   form_class = LoginForm
   def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_teacher:
                return reverse('instructor:index')  # 講師用のダッシュボードページのURL
            else:
                return reverse('student:children')  # 保護者用のダッシュボードページのURL
        else:
            return reverse('user:login')


class UserLogoutView(LogoutView):
    pass

class SignupUserView(CreateView):
   template_name = 'user/signup.html'
   form_class = SignupForm
   success_url = reverse_lazy('user:login')

   def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        while True:
            customer_id = str(random.randint(100000, 999999))
            if not User.objects.filter(customer_id=customer_id).exists():
                break
        user.customer_id = customer_id
        user.save()
        
        # ログインIDとパスワードを含むメールを送信
        subject = 'ご登録完了のお知らせ'
        context = {'username': user.username, 'customer_id': customer_id, 'password': form.cleaned_data['password']}
        message = render_to_string('e-mail/signup.html', context)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [form.cleaned_data['email']]
        email = EmailMessage(subject,message, from_email, recipient_list)
        email.content_subtype = 'html'
        email.send()

        # ログインページにリダイレクト
        messages.add_message(self.request, messages.SUCCESS ,'アカウントが作成されました。ログインしてください。')
        return response



@login_required
def contact(request,pk):
    student = get_object_or_404(Student,pk=pk)
    user = request.user
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']
            contact = Contact.objects.create(name=name, user=user, title=title, message=message)
            contact.save()
            return redirect('student:mypage' ,pk=pk)
    else:
        initial_data = {'name': student,"user":user.username, 'email': user.email}
        form = ContactForm(initial=initial_data)
    context = {
        'form': form,
        "student":student
    }
    return render(request, 'user/contact.html', context)


#-----------パスワードリセット----------



#----------------お知らせの確認-----------

def show_notifications(request,pk):
    student = get_object_or_404(Student,pk=pk)
    user = request.user
    notifications = user.notifications.all().order_by('-created_at')
    new_notifications = request.user.notifications.filter(is_new=True).order_by('-created_at')
    return render(request, 'student/notifications.html', {'notifications': notifications,"student":student,"new_notifications":new_notifications})

def view_notification(request, pk, notification_id):
    student = get_object_or_404(Student, pk=pk)
    notification = get_object_or_404(Notification, id=notification_id)

    # 既読情報を更新
    if notification.is_new and request.user in notification.recipients.all():
        notification.is_new = False
        notification.save()

    return render(request, 'student/notifications_detail.html', {'notification': notification, "student": student})
