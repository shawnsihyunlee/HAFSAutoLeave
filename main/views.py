from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tutorial
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
	init_data = {'student_id' : info.student_id, 'student_pass' : info.student_pass, 
				'out_day' : info.out_day, 'out_hour' : info.out_hour, 'out_minute' : info.out_minute,
				'return_day' : info.return_day, 'return_hour' : info.return_hour, 'return_minute' : info.return_minute}

	if request.method == "POST":
		# messages.success(request, "Clicked.")
		form = GoingInfoForm(request.POST, instance = info)
		if form.is_valid():
			info.do_auto_signup = not info.do_auto_signup
			saved_info = form.save()
			saved_info.refresh_from_db()
			is_active = saved_info.do_auto_signup
			if is_active == True:
				messages.success(request, "Activated auto-signup!")
			if is_active == False:
				messages.info(request, "Deactivated auto-signup!")
			# return redirect("main:homepage")
			return render(request = request,
				template_name = "main/home.html",
				context = {"form" : form, "is_active" : is_active})


	form = GoingInfoForm(instance = info, initial = init_data)
	is_active = info.do_auto_signup

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
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

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