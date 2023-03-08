from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.management.utils import get_random_secret_key
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password, make_password
from .models import Question, User, Session
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
            sessid = do_login(user.login, user.password)
            response = HttpResponseRedirect(reverse('new_questions'))
            response.set_cookie(
                'sessid',
                sessid,
                httponly=True,
                expires=datetime.now() + timedelta(days=5)
            )
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


def login(request):
    error = ''
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        sessid = do_login(login, password)
        if sessid:
            response = HttpResponseRedirect(reverse('new_questions'))
            response.set_cookie(
                'sessid',
                sessid,
                httponly=True,
                expires=datetime.now() + timedelta(days=5)
            )
            return response
        else:
            error = u'Неверный логин / пароль'
    return render(request, 'login.html', {'error': error})


def do_login(login, password):
    try:
        user = User.objects.get(login=login)
    except:
        return None

    hashed_pass = make_password(password)
    check_password(password, hashed_pass)
    session = Session(
        key=get_random_secret_key(),
        user=user,
        expires=datetime.now() + timedelta(days=5),
    )
    session.save()
    return session.key
