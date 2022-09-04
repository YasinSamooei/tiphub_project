from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager
#---------------------------------------------------------------------------------------------------------------
#customize User model

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='نشانی ایمیل',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(verbose_name="نام و نام خانوادگی", max_length=50,blank = True , null = True)
    username = models.CharField(verbose_name="نام کاربری", max_length=50,blank = True , null = True)
    is_active = models.BooleanField(default=True,verbose_name="کاربر فعال")
    is_admin = models.BooleanField(default=False,verbose_name="ادمین")
    phoneNumber = models.CharField(max_length=11,verbose_name="شماره تلفن",blank = True , null = True)
    image = models.ImageField(upload_to = "profiles/images" , blank = True , null = True,verbose_name="تصویر")
    is_teacher = models.BooleanField(default=False, verbose_name="مدرس")
    description = models.CharField(max_length=30,verbose_name="شرح حال", blank = True , null = True)
    instagram=models.URLField(verbose_name="آدرس پروفایل اینستاگرام", blank = True , null = True)
    telegram=models.URLField(verbose_name="آدرس پروفایل تلگرام", blank = True , null = True)
    linkdin=models.URLField(verbose_name="آدرس پروفایل لینکدین", blank = True , null = True)
    github=models.URLField(verbose_name="آدرس پروفایل گیت هاب", blank = True , null = True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD="email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name="کاربر"
        verbose_name_plural="کاربر ها"
#--------------------------------------------------------------------------------------------------------------------
class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE , related_name='notifs',verbose_name="کاربر")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="زمان ایجاد")
    title = models.CharField(max_length=30,verbose_name="عنوان")
    url=models.CharField(max_length=100,verbose_name="آدرس هدایت شدن")
    #Methods
    def __str__(self):
        return f"{self.user} , {self.title}"

    class Meta:
        verbose_name="خبر"
        verbose_name_plural="اخبار"
        ordering = ('-created_at',)
#--------------------------------------------------------------------------------------------------------------------


    