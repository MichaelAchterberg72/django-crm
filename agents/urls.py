from django.urls import path

from . import views
from .views import (
    AgentListView, AgentCreateView, AgentDetailView, AgentUpdateView, AgentDeleteView
)


app_name = 'Agents'


urlpatterns = [
    path('', AgentListView.as_view(), name='AgentsList'),
    path('create/', AgentCreateView.as_view(), name='AgentsCreate'),
    path('<int:pk>/', AgentDetailView.as_view(), name='AgentsDetail'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='AgentUpdate'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='AgentDelete'),
]
