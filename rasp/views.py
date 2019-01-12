from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rasp.models import Task, Work_category, ResponseOnTask
import datetime
from .forms import OrderForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json



TITLE_CHOICES = (('red', 'не готово'),
                 ('yellow', 'необходима проверка'),
                 ('green', 'готово')
                 )


@login_required(login_url='/login/')
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    num_authors = Task.objects.all().filter(status__contains='red', authors_name=request.user).order_by('-pub_date')

    categorys = Work_category.objects.all()
    now = datetime.datetime.now()

    context = {
        'num_authors': num_authors,
        'categorys': categorys,
        'now': now
    }
    return render(request, 'rasp/index.html', context,)


@login_required(login_url='/login/')
def index1(request, work_category_slug):
    categorys = Work_category.objects.all()
    categ = Work_category.objects.get(slug=work_category_slug)
    task_on_category = Task.objects.all().filter(authors_class=categ, authors_name=request.user, status__contains='red').order_by('-pub_date')
    now_time = datetime.datetime.now()
    context = {
        'categ': categ,
        'task_on': task_on_category,
        'categorys': categorys,
        'now': now_time
    }

    return render(request, 'rasp/task_cat.html', context,)


@login_required(login_url='/login/')
def task_view(request, task_slug):
    categorys = Work_category.objects.all()
    tas = Task.objects.get(slug1=task_slug)
    now_time = datetime.datetime.now()
    context = {
        'tas': tas,
        'categorys': categorys,
        'now': now_time
    }

    return render(request, 'rasp/task_res.html', context,)


@login_required(login_url='/login/')
def order_create_view(request, task_slug):
    categorys = Work_category.objects.all()
    tas = Task.objects.get(slug1=task_slug)
    form = OrderForm(request.POST or None)
    context = {
        'form': form,
        'tas': tas,
        'categorys': categorys
    }

    if form.is_valid():
        intro_text_responce = form.cleaned_data['intro_text_responce']
        responce_text = form.cleaned_data['responce_text']
        new_responce = ResponseOnTask.objects.create(
            responce_task=tas,
            user_responce=request.user,
            intro_text_responce=intro_text_responce,
            responce_text=responce_text,
            status_task=TITLE_CHOICES[1]
        )
        tas.status = TITLE_CHOICES[1]
        tas.save()
        return HttpResponseRedirect('/')
    return render(request, 'rasp/order.html', context)


@login_required(login_url='/login/')
def task_check_view(request):
    categorys = Work_category.objects.all()
    num_authors = Task.objects.all().filter(status__contains='yellow', authors_name=request.user).order_by('end_date')

    context = {
        'num_authors': num_authors,
        'categorys': categorys
    }
    return render(request, 'rasp/task_check.html', context,)


def login_view(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
        return HttpResponseRedirect('/')
    return render(request, 'rasp/autentification.html', context,)


'''class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all().filter()
    serializer_class = TaskSerializer


class TaskDetail(generics.RetrieveDestroyAPIView):
    slug_field = 'slud1'
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    

from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': request.user,  # `django.contrib.auth.User` instance.
            'auth': request.auth,  # None
        }
        return Response(content)


class SnippetList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly, IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.all().filter(authors_name=user)

    def perform_create(self, serializer):
        serializer.save(authors_name=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,     IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

'''


@csrf_exempt
def api_login(request):
    data = json.loads(request.body.decode())
    print(data)
    print(data['username'])
    user = User.objects.all().filter(username=data['username']).first()
    print(user)
    if user.check_password(data['password']):
        print('qwe')
        task1 = Task.objects.all().values('intro_text', 'task_text', 'pub_date', 'end_date').filter(authors_name=user)
        print(task1)
        for instance in task1:
            instance['pub_date'] = instance['pub_date'].strftime('%Y %m %d T%H:%M:%S')
            instance['end_date'] = instance['end_date'].strftime('%Y %m %d T%H:%M:%S')
        task = dict(zip((i for i in range(len(list(task1)))), (list(task1))))
        return JsonResponse(task)
