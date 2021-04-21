from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganiserAndLoginRequiredMixin
from django.http import HttpResponse
from django.views import generic

from .models import Contact, Category
from .forms import ContactForm, AssignAgentForm, ContactCategoryUpdateForm


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def landing_page(request):
    template = 'landing.html'
    return render(request, template)


class ContactListView(LoginRequiredMixin, generic.ListView):
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Contact.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = Contact.objects.filter(
                organisation=user.agent.organisation,
                agent__isnull=False
            )
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Contact.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                'unassigned_contacts': queryset
            })
        return context


def contact_list(request):
    contacts = Contact.objects.all()

    template = 'contacts/contact_list.html'
    context = {
        'contacts': contacts,
    }
    return render(request, template, context)


class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'contacts/contact_detail.html'
    context_object_name = 'contact'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Contact.objects.filter(organisation=user.userprofile)
        else:
            queryset = Contact.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset


def contactContactail(request, pk):
    contactContactontact.objects.get(pk=pk)

    template = 'contacts/contact_detail.html'
    context = {
        'contact': contact,
    }
    return render(request, template, context)


class ContactCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'contacts/contact_create.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('Contacts:ContactList')

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.organisation = self.request.user.userprofile
        contact.save()

        # TODO send email
        send_mail(
        subject='A contact has been created',
        message='Go to the site to see the new contact',
        from_email='test@test.com',
        recipient_list=['test2@test.com']
        )
        return super(ContactCreateView, self).form_valid(form)

def contact_create(request):
    form = ContactForm()
    if request.method == "POST":
        print('Receiving a post request')
        form = ContactForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect(reverse('ContactContactntactContact'))

    template = 'contacts/contact_create.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


class ContactUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'contacts/contact_update.html'
    queryset = Contact.objects.all()
    form_class = ContactForm

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse('Contacts:ContactList')


def contact_update(request, pk):
    contact = Contact.objects.get(pk=pk)
    form = ContactForm(instance=contact)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return reverse('Contact:Home')

    template = 'contacts/contact_update.html'
    context = {
        'contact': contact,
        'form': form,
    }
    return render(request, template, context)


class ContactDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'contacts/contact_delete.html'

    def get_success_url(self):
        return reverse('Contacts:ContactList')

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(organisation=user.userprofile)


def contact_delete(request, pk):
    contact = Contact.objects.get(pk=pk)
    contact.delete()
    return reverse('Contact:Home')


#class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = 'contacts/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse('Contacts:ContactList')

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        contact = Contact.objects.get(id=self.kwargs["pk"])
        contact.agent = agent
        contact.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'contacts/category_list.html'
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Contact.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Contact.objects.filter(
                organisation=user.agent.organisation
            )
        context.update({
            "unassigned_contact_count": queryset.filter(category__isnull=True).count()
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
    template_name = 'contacts/category_detail.html'
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


class ContactCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'contacts/contact_category_update.html'
    queryset = Contact.objects.all()
    form_class = ContactCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Contact.objects.filter(organisation=user.userprofile)
        else:
            queryset = Contact.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('Contacts:ContactDetail', kwargs={"pk": self.get_object().id})
