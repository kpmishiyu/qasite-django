from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import QuestionForm, SignUpForm, AnswerForm
from .models import Question, Profile, Answer

# Create your views here.

def homepage(request):
    # 从 URL 参数中获取'sort'的值，如果没找到，就默认使用'time'
    sort_option = request.GET.get('sort', 'time')

    if sort_option == 'bounty':
        # 如果是 'bounty', 就按 bounty 字段降序排列
        questions = Question.objects.order_by('-bounty')
    else:
        # 否则（包括 'time' 和其他任何情况），都按 created_at 字段降序排列
        questions = Question.objects.order_by('-created_at')

    context = {
        'questions': questions,
        'sort_option': sort_option, # 把当前的排序方式也传递给模板
    }
    return render(request, 'core/index.html', context)
@login_required
def ask_question(request):
    if request.method == 'POST':
        # 这里是关键修改：同时接收 POST 数据和 FILES 文件数据
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('homepage')
    else:
        form = QuestionForm()
    return render(request, 'core/ask_question.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            # 这里是关键修改：同时接收 POST 数据和 FILES 文件数据
            answer_form = AnswerForm(request.POST, request.FILES)
            if answer_form.is_valid():
                new_answer = answer_form.save(commit=False)
                new_answer.question = question
                new_answer.author = request.user
                new_answer.save()
                return redirect('question_detail', pk=question.pk)
        else:
            return redirect('login')
    else:
        answer_form = AnswerForm()

    context = {
        'question': question,
        'answers': answers,
        'answer_form': answer_form,
    }
    return render(request, 'core/question_detail.html', context)

@login_required
def accept_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    question = answer.question

    if request.user != question.author:
        return HttpResponseForbidden("你没有权限执行此操作。")

    if not question.is_resolved:
        question_author_profile = question.author.profile
        answer_author_profile = answer.author.profile

        bounty = question.bounty
        
        if question_author_profile.coins >= bounty:
            question_author_profile.coins -= bounty
            answer_author_profile.coins += bounty

            question.is_resolved = True

            question_author_profile.save()
            answer_author_profile.save()
            question.save()

    return redirect('question_detail', pk=question.pk)
@login_required
def my_profile(request):
    # 获取当前登录用户发布的所有问题
    my_questions = Question.objects.filter(author=request.user).order_by('-created_at')

    # 获取当前登录用户提交的所有回答
    # __distinct=True 确保即使对同一个问题有多个回答，问题也只显示一次
    my_answers = Answer.objects.filter(author=request.user).order_by('-created_at')

    context = {
        'my_questions': my_questions,
        'my_answers': my_answers,
    }
    return render(request, 'core/my_profile.html', context)