from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Question
from .forms import AskForm, AnswerForm

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
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save()
            url = answer.question.get_url()
            return HttpResponseRedirect(url)
    else:
        question = get_object_or_404(Question, pk=pk)

        return render(
            request=request,
            template_name='qa/question_details.html',
            context={
                'form': AnswerForm(initial={"question": question.pk}),
                'question': question
            }
        )


def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        return render(
            request=request,
            template_name='qa/ask.html',
            context={
                'form': AnswerForm(),
            }
        )


def test(request, *args, **kwargs):
    return HttpResponse('OK')
