from django.shortcuts import render, redirect
from .forms import RegisterForm,ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from results.models import Result
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        # print(form.errors)
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form":form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("home")
        else:
            print(form.errors)

        

    

    

    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html",{"form":form})
@login_required
def dashboard(request):

    results = Result.objects.filter(user=request.user)

    total_quizzes = results.count()

    highest_score = 0

    for result in results:
        if result.score > highest_score:
            highest_score = result.score

    

    return render(request, "accounts/dashboard.html", {
        "results":results,
        "total_quizzes":total_quizzes,
        "highest_score":highest_score,
    })
def user_logout(request):
    logout(request)
    return redirect("home")
@login_required
def profile(request):
    return render(request,"accounts/profile.html")

@login_required
def edit_profile(request):

    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:

        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form
        }
    )

@login_required
def quiz_history(request):

    results = Result.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "accounts/quiz_history.html",
        {
            "results": results
        }
    )

# Create your views here.
