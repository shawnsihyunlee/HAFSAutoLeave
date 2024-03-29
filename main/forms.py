from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import GoingInfo


class NewUserForm(UserCreationForm):
    # username = forms.CharField(label='아이디', min_length=4, max_length=150, required=True)
    # password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput, required=True)
    # password2 = forms.CharField(label='비밀번호 재입력', widget=forms.PasswordInput, 
    #                             help_text = "Enter the same password as above, for verification.", 
    #                             required=True)
    email = forms.EmailField(label = "이메일", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class GoingInfoForm(forms.ModelForm):

    day_choices = [("friday", "Friday"), ("saturday", "Saturday"), ("sunday", "Sunday")]
    minute_choices = [(x, x) for x in range(0, 70, 10)]
    hour_choices = [(x, x) for x in range(0, 24)]

    out_day= forms.CharField(label='Out day', widget=forms.Select(choices=day_choices, attrs = {"class" : "browser-default"}))
    return_day= forms.CharField(widget=forms.Select(choices=day_choices, attrs = {"class" : "browser-default"}))
    out_hour= forms.IntegerField(widget=forms.Select(choices=hour_choices, attrs = {"class" : "browser-default"}))
    out_minute= forms.IntegerField(widget=forms.Select(choices=minute_choices, attrs = {"class" : "browser-default"}))
    return_hour= forms.IntegerField(widget=forms.Select(choices=hour_choices, attrs = {"class" : "browser-default"}))
    return_minute= forms.IntegerField(widget=forms.Select(choices=minute_choices, attrs = {"class" : "browser-default"}))
    class Meta:
        model = GoingInfo
        fields = ['student_id', 'student_pass', 
                  'out_day', 'out_hour', 'out_minute',
                  'return_day', 'return_hour', 'return_minute', 'leave_number']

    def clean_leave_number(self):
        data = self.cleaned_data['leave_number']
        if data <= 0 and data != -69:
            raise forms.ValidationError("Enter a valid leave number!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data






 
# class CustomUserCreationForm(UserCreationForm):
#     username = forms.CharField(label='아이디', min_length=4, max_length=150)
#     password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='비밀번호 재입력', widget=forms.PasswordInput)
 
#     def clean_username(self):
#         username = self.cleaned_data['username'].lower()
#         r = User.objects.filter(username=username)
#         if r.count():
#             raise  ValidationError("Username already exists")
#         return username
 
#     def clean_email(self):
#         email = self.cleaned_data['email'].lower()
#         r = User.objects.filter(email=email)
#         if r.count():
#             raise  ValidationError("Email already exists")
#         return email
 
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Password don't match")
#         return password2
 
#     def save(self, commit=True):
#         user = User.objects.create_user(
#             self.cleaned_data['username'],
#             self.cleaned_data['email'],
#             self.cleaned_data['password1']
#         )

#         return user