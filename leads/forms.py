from django import forms
from .models import Lead, Agent


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = {'first_name', 'last_name', 'age', 'agent', 'description',     'phone_number', 'email'}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = {'category',}
