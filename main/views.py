from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, GoingInfoForm


# Create your views here.

def homepage(request):
	curr_user = request.user
	if not curr_user.is_authenticated:
		messages.info(request, "Please login first.")
		return redirect("main:login")

	info = request.user.goinginfo

	
	is_active = info.do_auto_signup
	

	init_data = {'student_id' : info.student_id, 'student_pass' : info.student_pass, 
				'out_day' : info.out_day, 'out_hour' : info.out_hour, 'out_minute' : info.out_minute,
				'return_day' : info.return_day, 'return_hour' : info.return_hour, 'return_minute' : info.return_minute}

	if request.method == "POST":
		# messages.success(request, "Clicked.")
		form = GoingInfoForm(request.POST, instance = info)
		if not is_active:
			if form.is_valid():
				info.do_auto_signup = not info.do_auto_signup
				saved_info = form.save()
				# saved_info.refresh_from_db()
				# is_active = True if saved_info.leave_number > 0 else False

				messages.success(request, "자동외출을 실행했습니다!")
			else:
				messages.error(request, "자동 외출 횟수는 0 이상이어야 합니다.")

		else:
			info.do_auto_signup = not info.do_auto_signup
			info.save()
			messages.info(request, "자동외출을 해제했습니다.")
				
		return redirect("main:homepage")
		# return render(request = request,
		# 	template_name = "main/home.html",
		# 	context = {"form" : form, "is_active" : is_active})


	form = GoingInfoForm(instance = info, initial = init_data)
	
	if is_active:
		form.fields['student_id'].widget.attrs['disabled'] = True
		form.fields['student_pass'].widget.attrs['disabled'] = True
		form.fields['out_day'].widget.attrs['disabled'] = True
		form.fields['out_hour'].widget.attrs['disabled'] = True
		form.fields['out_minute'].widget.attrs['disabled'] = True
		form.fields['return_day'].widget.attrs['disabled'] = True
		form.fields['return_hour'].widget.attrs['disabled'] = True
		form.fields['return_minute'].widget.attrs['disabled'] = True
		form.fields['leave_number'].widget.attrs['disabled'] = True

	else:
		form.fields['student_id'].widget.attrs['disabled'] = False
		form.fields['student_pass'].widget.attrs['disabled'] = False
		form.fields['out_day'].widget.attrs['disabled'] = False
		form.fields['out_hour'].widget.attrs['disabled'] = False
		form.fields['out_minute'].widget.attrs['disabled'] = False
		form.fields['return_day'].widget.attrs['disabled'] = False
		form.fields['return_hour'].widget.attrs['disabled'] = False
		form.fields['return_minute'].widget.attrs['disabled'] = False
		form.fields['leave_number'].widget.attrs['disabled'] = False

	return render(request = request,
				  template_name = "main/home.html",
				  context = {"form" : form, "is_active" : is_active})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"비밀번호가 일치하지 않거나 너무 짧습니다.")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("main:login")

def login_request(request):
	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect('/')
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request, "main/login.html", context = {"form" : form})
