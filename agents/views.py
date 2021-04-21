import random

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from .mixins import OrganiserAndLoginRequiredMixin

from .models import Agent

from .forms import AgentModelForm


class AgentListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('Agents:AgentsList')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f'{random.randint(0, 1000)}')
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        #TODO create tyhe agent created  regisdtration login email
        send_mail(
            from_email="admin@crm.com",
            recipient_list=[user.email],
            subject="You are invited to be an agent",
            message="You were added as an agent on CRM. Please come login to start working."
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('Agents:AgentsList')

    def get_queryset(self):
        return Agent.objects.all()


class AgentDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse('Agents:AgentsList')

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
