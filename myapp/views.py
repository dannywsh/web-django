from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect,Http404,get_object_or_404
from django.urls import reverse
from django.views import generic
# Create your views here.

from .models import Question,Choice # 从models导入
#user_list = []

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

class IndexView(generic.ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'myapp/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'myapp/results.html'

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

