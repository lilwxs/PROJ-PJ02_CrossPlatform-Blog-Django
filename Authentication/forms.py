import datetime
import re
from django import forms
from Authentication.models import CusUser
from django.db.models import Q
from django.core.exceptions import ValidationError

class UserLoginForm(forms.ModelForm):
    OneEmailOrUsername = forms.CharField(label='Email or Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

    def clean_OneEmailOrUsername(self):
        OneEmailOrUsername = self.cleaned_data.get('OneEmailOrUsername')
        if OneEmailOrUsername is None:
            raise ValidationError("Email hoặc Username không được để trống.")
        if ' ' in OneEmailOrUsername:
            raise ValidationError("Email hoặc Username không được có khoảng trắng.")
        try:
            user = CusUser.objects.get(Q(email=OneEmailOrUsername) | Q(username=OneEmailOrUsername))
            return user.username or user.email
        except CusUser.DoesNotExist:
            raise ValidationError("Tài khoản không tồn tại.")

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password is None:
            raise ValidationError("Mật khẩu không được để trống.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = CusUser
        fields = ['OneEmailOrUsername', 'password']

class UserRegisterForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100, widget=forms.TextInput)
    last_name = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput)
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput)
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput)
    gender = forms.ChoiceField(label='Gender', choices=[('0', 'Nam'), ('1', 'Nữ'), ('2', 'Khác')], widget=forms.RadioSelect)
    birthday = forms.DateField(label='Birthday', widget=forms.SelectDateWidget(years=range(1900, datetime.datetime.now().year + 1)))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', max_length=100, widget=forms.PasswordInput)

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name is None:
            raise ValidationError("Tên không được để trống.")
        if re.search(r'[^A-Za-z][0-9]', first_name):
            raise ValidationError("Tên không được có ký tự đặc biệt.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name is None:
            raise ValidationError("Họ không được để trống.")
        if re.search(r'[^A-Za-z][0-9]', last_name):
            raise ValidationError("Họ không được có ký tự đặc biệt.")
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is None:
            raise ValidationError("Username không được để trống.")
        if ' ' in username:
            raise ValidationError("Username không được có khoảng trắng.")
        if not username.isalnum():
            raise ValidationError("Username không được có ký tự đặc biệt.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise ValidationError("Email không được để trống.")
        if '@' not in email:
            raise ValidationError("Email không hợp lệ.")
        return email

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday is None:
            raise ValidationError("Ngày sinh không được để trống.")
        return birthday

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender is None:
            raise ValidationError("Giới tính không được để trống.")
        return gender

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password is None:
            raise ValidationError("Mật khẩu không được để trống.")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        if confirm_password is None:
            raise ValidationError("Xác nhận mật khẩu không được để trống.")
        return confirm_password

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise ValidationError("Mật khẩu xác nhận không khớp.")
        return cleaned_data

    def save(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        gender = self.cleaned_data.get('gender')
        birthday = self.cleaned_data.get('birthday')
        password = self.cleaned_data.get('password')
        user = CusUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, gender=gender, birthday=birthday, password=password)
        return user

    class Meta:
        model = CusUser
        fields = ['first_name', 'last_name', 'username', 'email', 'gender', 'birthday', 'password', 'confirm_password']

class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Mật khẩu cũ', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu cũ'}))
    new_password = forms.CharField(label='Mật khẩu mới', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu mới'}))
    confirm_password = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError('Mật khẩu mới và xác nhận mật khẩu không khớp.')
        return cleaned_data

    def save(self, user):
        user.set_password(self.cleaned_data.get('new_password'))
        user.save()
        return user

    class Meta:
        model = CusUser
        fields = ['old_password', 'new_password', 'confirm_password']
