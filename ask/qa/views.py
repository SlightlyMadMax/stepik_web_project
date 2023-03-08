from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from .models import Question
from .forms import AskForm, AnswerForm, SignUpForm
from datetime import timedelta, datetime


@require_GET
def new_questions(request):
    limit = 10

    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    paginator = Paginator(Question.objects.new(), limit)
    page = paginator.page(page)

    return render(
        request=request,
        template_name='qa/questions.html',
        context={
            'questions': page.object_list,
            'paginator': paginator,
            'page': page,
        }
    )


@require_GET
def popular_questions(request):
    limit = 10

    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    paginator = Paginator(Question.objects.popular(), limit)
    page = paginator.page(page)

    return render(
        request=request,
        template_name='qa/questions.html',
        context={
            'questions': page.object_list,
            'paginator': paginator,
            'page': page,
        }
    )


def question_details(request, pk: int):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST, user=request.user)
        if form.is_valid():
            _ = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={"question": question.pk}, user=request.user)
    return render(
        request=request,
        template_name='qa/question_details.html',
        context={
            'form': form,
            'question': question
        }
    )


def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST, user=request.user)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(user=request.user)
    return render(
        request=request,
        template_name='qa/ask.html',
        context={
            'form': form,
        }
    )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(login=user.login, password=user.password)
            login(request, user)
            response = HttpResponseRedirect(reverse('new_questions'))
            return response
    else:
        form = SignUpForm()
    return render(
        request=request,
        template_name='qa/signup.html',
        context={
            'form': form,
        }
    )


def login_view(request):
    error = ''
    if request.method == 'POST':
        user_login = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(login=user_login, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('new_questions'))
        else:
            error = u'Неверный логин / пароль'
    return render(request, 'login.html', {'error': error})

