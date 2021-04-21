from django import forms
from .models import Contact, Agent


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = {'first_name', 'last_name', 'age', 'agent', 'description',     'phone_number', 'email'}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class ContactCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = {'category',}
