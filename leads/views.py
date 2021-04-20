from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganiserAndLoginRequiredMixin
from django.http import HttpResponse
from django.views import generic

from .models import Lead, Category
from .forms import LeadForm, AssignAgentForm, LeadCategoryUpdateForm


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def landing_page(request):
    template = 'landing.html'
    return render(request, template)


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation,
                agent__isnull=False
            )
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                'unassigned_leads': queryset
            })
        return context


def lead_list(request):
    leads = Lead.objects.all()

    template = 'leads/lead_list.html'
    context = {
        'leads': leads,
    }
    return render(request, template, context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset


def lead_detail(request, pk):
    lead = Lead.objects.get(pk=pk)

    template = 'leads/lead_detail.html'
    context = {
        'lead': lead,
    }
    return render(request, template, context)


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadForm

    def get_success_url(self):
        return reverse('Leads:LeadList')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()

        # TODO send email
        send_mail(
        subject='A lead has been created',
        message='Go to the site to see the new lead',
        from_email='test@test.com',
        recipient_list=['test2@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)

def lead_create(request):
    form = LeadForm()
    if request.method == "POST":
        print('Receiving a post request')
        form = LeadForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect(reverse('Leads:LeadList'))

    template = 'leads/lead_create.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all()
    form_class = LeadForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse('Leads:LeadList')


def lead_update(request, pk):
    lead = Lead.objects.get(pk=pk)
    form = LeadForm(instance=lead)
    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return reverse('Lead:Home')

    template = 'leads/lead_update.html'
    context = {
        'lead': lead,
        'form': form,
    }
    return render(request, template, context)


class LeadDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_success_url(self):
        return reverse('Leads:LeadList')

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)


def lead_delete(request, pk):
    lead = Lead.objects.get(pk=pk)
    lead.delete()
    return reverse('Lead:Home')


#class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse('Leads:LeadList')

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_category_update.html'
    queryset = Lead.objects.all()
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('Leads:LeadDetail', kwargs={"pk": self.get_object().id})
