from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.core.paginator import Paginator
from models import Question


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
def popular_question(request):
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


@require_GET
def question_details(request, pk: int):
    question = get_object_or_404(Question, pk)

    return render(
        request=request,
        template_name='qa/question_details.html',
        context={
            'question': question
        }
    )


def test(request, *args, **kwargs):
    return HttpResponse('OK')
