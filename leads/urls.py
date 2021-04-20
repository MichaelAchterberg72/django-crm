from django.urls import path

from .import views
from .views import (
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, AssignAgentView, CategoryListView, CategoryDetailView, LeadCategoryUpdateView
)


app_name = 'Leads'


urlpatterns = [
    path('', LeadListView.as_view(), name='LeadList'),
    path('create/', LeadCreateView.as_view(), name='LeadCreate'),
    path('<int:pk>/', LeadDetailView.as_view(), name='LeadDetail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='LeadUpdate'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='LeadDelete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='AssignAgent'),
    path('categories/', CategoryListView.as_view(), name='CategoryList'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='CategoryDetail'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='LeadCategoryUpdate'),
]
