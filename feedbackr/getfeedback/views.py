from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from getfeedback.models import QuestionSet, YesNoQuestion
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
import base64
from django.views.decorators.http import require_POST


def get_qs_name(username):
    current_time = datetime.now()
    current_time_string = current_time.strftime("%Y-%m-%d-%H:%M:%S")
    return current_time_string + "-" + username


@login_required
def upload(request):
    data = {}
    if "GET" == request.method:
        return render(request, "getfeedback/upload.html", data)
    csv_file = request.FILES["csv_file"]
    if csv_file.multiple_chunks():
        return HttpResponse("File too large", status=413)
    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")
    username = request.user.username
    qs = QuestionSet.objects.create(
        description=get_qs_name(username), creator=request.user
    )
    created = []
    for l in lines:
        parts = l.split(",")
        if len(parts) < 2:
            for qu in created:
                qu.delete()
            qs.delete()
            return HttpResponse("File must be a comma delimited plain text file with at least 2 columns for prompt and completion", status=400)
        prompt = str(parts[0])
        completion = str(parts[1])
        if len(prompt) > 1999 or len(completion) > 1999:
            for qu in created:
                qu.delete()
            qs.delete()
            return HttpResponse("Both prompt and completion should be less than 400 characters", status=400)
        q = YesNoQuestion.objects.create(prompt=prompt, completion=completion, question_set=qs)
        created.append(q)
    return HttpResponseRedirect(reverse("myqs"))


@login_required
def my_qs(request):
    qs = QuestionSet.objects.filter(creator=request.user)
    return render(request, "getfeedback/my_qs.html", {"qs": qs})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "getfeedback/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def home(request):
    return render(request, "getfeedback/home.html")


def details(request, id):
    try:
        qs = QuestionSet.objects.get(pk=id)
        if qs.creator != request.user:
            return HttpResponse(
                "You do not have permisison to access this set", status=403
            )
        questions = YesNoQuestion.objects.filter(question_set=qs)
        return render(request, "getfeedback/details.html", {"questions": questions})
    except QuestionSet.DoesNotExist:
        return HttpResponse("Question set not found", status=404)


def answer(request, id):
    try:
        qs = QuestionSet.objects.get(pk=id)
        questions = YesNoQuestion.objects.filter(question_set=qs)
        return render(request, "getfeedback/answer.html", {"questions": questions})
    except QuestionSet.DoesNotExist:
        return HttpResponse("Question set not found", status=404)

@require_POST
def vote_yes(request):
    id = request.POST.get('id', '')
    instance = get_object_or_404(YesNoQuestion, pk=id)
    instance.yes_votes += 1
    instance.save()
    return HttpResponse(status=200)

@require_POST
def vote_no(request):
    id = request.POST.get('id', '')
    instance = get_object_or_404(YesNoQuestion, pk=id)
    instance.no_votes += 1
    instance.save()
    return HttpResponse(status=200)
