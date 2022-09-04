from django.contrib.auth.forms import ReadOnlyPasswordHashField,UserCreationForm  
from django.core.exceptions import ValidationError
from django import forms
from accounts.models import User
#--------------------------------------------------------------------------------------
# User forms
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=' رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name','username','phoneNumber','image','is_active','is_teacher')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'is_active', 'is_admin','username','phoneNumber','image','is_teacher')

#---------------------------------------------------------------------------------------------------------------------------
class LoginForm(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={"class":"email-input","placeholder":"پست الکترونیک","maxlength":50}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"password-input","placeholder":"گذرواژه"}))
#---------------------------------------------------------------------------------------------------------------------------
class RegisterForm(UserCreationForm):  
    email =forms.CharField(widget=forms.EmailInput(attrs={"class":"email-input","placeholder":"پست الکترونیک","maxlength":50,"dir":"rtl"}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"password-input","placeholder":"گذرواژه","dir":"rtl"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"password-input","placeholder":"تکرار گذرواژه","dir":"rtl"}))
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"text-input","placeholder":"نام کاربری","dir":"rtl"}))
    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')  
#---------------------------------------------------------------------------------------------------------------------------
class EditUserForm(forms.ModelForm):  
    email =forms.CharField(widget=forms.EmailInput(attrs={"class":"email-input","placeholder":"پست الکترونیک","maxlength":50}))
    full_name=forms.CharField(widget=forms.TextInput(attrs={"class":"email-input","placeholder":"نام و نام خانوادگی","maxlength":70}))
    phoneNumber=forms.IntegerField(widget=forms.TextInput(attrs={"class":"email-input","placeholder":"شماره تلفن","maxlength":11}))
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"","placeholder":"نام کاربری","maxlength":50}))
    image=forms.ImageField(widget=forms.FileInput(attrs={'id':"select-files", 'accept':"image/*", 'data-val':"true", 'data-val-fileimage':"شما فقط قادر به انتخاب عکس می باشید",  'data-val-filesize':"حجم فایل بیشتر از 5 مگابایت می باشید" ,'filesize':"5120",'type':"file" ,'hidden':""}))
    def __init__(self,*args,**kwargs):
        super(EditUserForm,self).__init__(*args,**kwargs)
        self.fields['email'].disabled=True

    class Meta:  
        model = User  
        fields = ('username', 'email', 'full_name', 'phoneNumber','image') 
#-----------------------------------------------------------------------------------------------------------------------------
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None
		
        if not user.is_admin:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['is_teacher'].disabled = True

    class Meta:
        model = User
        fields = ['username', 'email','full_name','is_teacher','github','description','linkdin','telegram','instagram','image']