from django import forms

from .models import Resturant, User


class ResturantModelForm(forms.ModelForm):
    class Meta:
        model = Resturant
        fields = [
            'name',
            'address',
            'res_image',
        ]

    def has_img(self):
        img = self.cleaned_data.get('res_image')
        if not img:
            raise forms.ValidationError("没有图片信息!")
        return img


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, *kwargs)
        self.fields['username'].label = '用户名'
        self.fields['password'].label = '密码'


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="邮箱", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="昵称", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))


class CommentForm(forms.Form):
    content = forms.CharField(max_length=255, label="评论", widget=forms.TextInput(attrs={'class': 'form-control'}))
    rate_taste = forms.DecimalField(max_digits=3, decimal_places=2, label="口味", widget=forms.Select(attrs={'class': 'form-control'}))
    rate_surround = forms.DecimalField(max_digits=3, decimal_places=2, label="环境", widget=forms.Select(attrs={'class': 'form-control'}))
    rate_service = forms.DecimalField(max_digits=3, decimal_places=2, label="服务", widget=forms.Select(attrs={'class': 'form-control'}))