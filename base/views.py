from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    templates_name = 'registration/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('base:Tasklist')

class RegisterPage(generic.FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('base:Tasklist')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('base:Tasklist')
        return super(RegisterPage, self).get(*args, **kwargs)

class Tasklist(LoginRequiredMixin, generic.ListView):
    model = Task
    templates_name = 'base/task_list.html'
    context_object_name = 'Tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Tasks'] = context['Tasks'].filter(user=self.request.user)
        context['count'] = context['Tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['Tasks'] = context['Tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, generic.DetailView):
    model = Task
    templates_name =  'base/task_detail.html'

class TaskCreate(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('base:Tasklist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('base:Tasklist')

class TaskDelete(LoginRequiredMixin, generic.DeleteView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('base:Tasklist')

