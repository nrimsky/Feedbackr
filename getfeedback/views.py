from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from getfeedback.models import QuestionSet, YesNoQuestion
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.views.decorators.http import require_POST
from django.db.models.functions import Random



def get_qs_name(username):
    current_time = datetime.now()
    current_time_string = current_time.strftime("%Y-%m-%d-%H:%M:%S")
    return current_time_string + "-" + username


@login_required
def upload(request):
    data = {}
    if "GET" == request.method:
        return render(request, "getfeedback/upload.html", data)
    json_file = request.FILES["json_file"]
    if json_file.multiple_chunks():
        return HttpResponse("File too large", status=413)
    file_data = json_file.read().decode()
    qs = None
    try:
        all_data = json.loads(file_data)
        data = all_data["data"]
        name = all_data.get("name", get_qs_name(request.user.username))
        qs = QuestionSet.objects.create(
            description=name, creator=request.user
        )
        valid_data = []
        for d in data:
            if len(d["prompt"]) < 1999 and len(d["completion"]) < 1999:
                valid_data.append((d["prompt"], d["completion"]))
            else:
                return HttpResponse("Both prompt and completion should be less than 2000 characters", status=400)
        for p, c in valid_data:
            YesNoQuestion.objects.create(prompt=p, completion=c, question_set=qs)
    except Exception as e:
        print(e)
        if qs is not None:
            qs.delete()
        return HttpResponse("File must be a JSON with top level keys data and name. Data should contain an array of objects with keys prompt and completion", status=400)
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
        order = request.GET.get('order')
        if order == 'random':
            questions = questions.annotate(random_order=Random()).order_by('random_order')
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
