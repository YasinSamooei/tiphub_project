from django.db import models
from accounts.models import User
from django.urls import reverse
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from extensions.utils import jalali_converter
from django.utils.html import format_html
from django.utils import timezone
from .managers import ArticleManager,CategoryManager
from comment.models import Comment
from django.forms import ValidationError
#-------------------------------------------------------------------------------------------------------------

class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name="زیردسته")
    title = models.CharField(max_length=200, verbose_name="عنوان دسته‌بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته‌بندی",allow_unicode=True)
    status = models.BooleanField(default=True, verbose_name="وضعیت نمایش")
    position = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی ها"
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title
    
    def get_categories(self):
         if self.parent is None:
            return self.title
         else:
            return self.title + ' -> ' + self.parent.get_categories()
    get_categories.short_description = "موضوع"
    objects = CategoryManager()
#--------------------------------------------------------------------------------------------------------------
class Video(models.Model):
    STATUS_CHOICES = (
        ('p', "منتشر شده"),		 # publish
        ('i', "در حال بررسی"),	 # investigation
        ('b', "برگشت داده شده"), # back
    )
    auther = models.ForeignKey(User , on_delete=models.CASCADE,verbose_name="مدرس")
    category = models.ManyToManyField(Category , related_name="posts",verbose_name="دسته بندی")
    title = models.CharField(max_length=30,verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    time=models.CharField(max_length=50,verbose_name="زمان ویدئو")
    video = models.FileField(upload_to = 'videos',verbose_name="ویدئو")
    image=models.ImageField(upload_to='VideosImage',verbose_name="تصویر جلد")
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    date = models.DateTimeField(auto_now_add=True,verbose_name="زمان ایجاد")
    update = models.DateTimeField(auto_now=True,verbose_name="به روز رسانی")
    slug = models.SlugField(unique=True,verbose_name="آدرس",allow_unicode=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',related_query_name='hit_count_generic_relation')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
    comments = GenericRelation(Comment)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:videodetail' , args=[self.slug])

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "زمان انتشار"

    def show_img(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="100px" height="70px">')
        else:
            return format_html("<h3>تصویر ندارد</h3>")
    show_img.short_description="تصویر پست"

    def category_to_str(self):
        return "، ".join([category.title for category in self.category.active()])
    category_to_str.short_description = "دسته‌بندی"

    class Meta:
        ordering = ('-date',)
        verbose_name = 'فیلم'
        verbose_name_plural="فیلم ها"

    objects = ArticleManager()
#--------------------------------------------------------------------------------------------------------------

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE , related_name='likes',verbose_name="کاربر")
    video=models.ForeignKey(Video,on_delete=models.CASCADE , related_name='likes',verbose_name="ویدئو")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="زمان ایجاد")

    #Methods
    def __str__(self):
        return f"{self.user} , {self.video}"

    class Meta:
        verbose_name="پسند"
        verbose_name_plural="پسندها "
        ordering = ('created_at',)

#--------------------------------------------------------------------------------------------------------------
class Logo(models.Model):
    image=models.ImageField(upload_to='logo',verbose_name="لوگو",default="../static/image/logo.png")
    def show_img(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="100px" height="70px">')
        else:
            return format_html("<h3>تصویر ندارد</h3>")
    show_img.short_description="تصویر پست"

    def save(self, *args, **kwargs):
        if not self.pk and Logo.objects.exists():
            raise ValidationError('فقط حق انتخاب یک نمونه را دارید')
        return super(Logo, self).save(*args, **kwargs)
    class Meta:
        verbose_name="لوگو"
        verbose_name_plural="لوگو ها "