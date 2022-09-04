from django.shortcuts import redirect, render
from django.contrib.auth import login , logout, authenticate
from django.urls import reverse_lazy
from accounts.models import User
from django.http import HttpResponse  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import LoginForm,RegisterForm,EditUserForm      
from django.views.generic import View,UpdateView,CreateView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from.forms import ProfileForm
from django.contrib.auth.views import( PasswordChangeView,PasswordResetView,
PasswordResetConfirmView,PasswordResetDoneView)
#------------------------------------------------------------------------------------------------------------------
#logout
def user_logout(request):
    logout(request)
    return redirect('/')

#------------------------------------------------------------------------------------------------------------------

# login
class UserLogin(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            form=LoginForm()
            return render(request,"accounts/login.html",{"form":form})
    
    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(username=cd['email'],password=cd['password'])
            if user is not None:
                login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                return redirect("/")
            else:
                form.add_error("email","اطلاعات کاربری صحیح نمی باشد")
        else:
            form.add_error("email","اطلاعات ارسالی صحیح نمی باشد")
        return render(request,"accounts/login.html",{"form":form})


#---------------------------------------------------------------------------------------
def user_info(request):
    if request.user.is_admin or request.user.is_teacher:
        return redirect("accounts:profile")
    else:
        return render(request , "accounts/user-panel.html")
#---------------------------------------------------------------------------------------
class EditProfileView(UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'accounts/edit-user-panel.html'
    success_url = reverse_lazy('account:userpanel')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
# Register View
class UserRegister(CreateView):
    form_class=RegisterForm
    template_name="accounts/register.html"
    
    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('accounts/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request,"accounts/send-email.html")

#--------------------------------------------------------------------------------------------------------------------------

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return render(request,"accounts/active_account_complete.html")
    else:
        return HttpResponse('<a href="accounts/register">دوباره امتحان کنید</a> لینک فعال سازی منقضی شده است ! ')
#-------------------------------------------------------------------------------------------------------------------------------------

class PasswordChange(PasswordChangeView):
    success_url=reverse_lazy("accounts:password_change_done")
class PasswordReset(PasswordResetView):
    success_url=reverse_lazy("accounts:password_reset_done")
class PasswordResetDone(PasswordResetDoneView):
    success_url=reverse_lazy("accounts:password_reset_confirm")
class PasswordResetConfirm(PasswordResetConfirmView):
    success_url=reverse_lazy("accounts:password_reset_complete")


class Profile(LoginRequiredMixin ,UpdateView):
    model = User
    template_name = "registration/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs