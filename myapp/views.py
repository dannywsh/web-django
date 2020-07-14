from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect,Http404,get_object_or_404
from django.urls import reverse
# Create your views here.

from myapp import models  # 导入models文件
from .models import Question
#user_list = []

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'myapp/index.html', context)

'''
def index(request):
    #return HttpResponse('Hello world')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 将数据保存到数据库
        models.UserInfo.objects.create(user=username, pwd=password)
        
        # 从数据库中读取所有数据，注意缩进
    user_list = models.UserInfo.objects.all()
    return render(request,'index.html',{'data':user_list})
'''

def detail(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    #return HttpResponse("You're looking at question %s." % question)
    return render(request,'myapp/detail.html',{'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):     
        return render(request, 'myapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()       
        return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))

