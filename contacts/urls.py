from django.urls import path

from .import views
from .views import (
    ContactListView, ContactDetailView, ContactCreateView, ContactUpdateView, ContactDeleteView, AssignAgentView, CategoryListView, CategoryDetailView, ContactCategoryUpdateView
)


app_name = 'Contacts'


urlpatterns = [
    path('', ContactListView.as_view(), name='ContactList'),
    path('create/', ContactCreateView.as_view(), name='ContactCreate'),
    path('<int:pk>/', ContactDetailView.as_view(), name='ContactDetail'),
    path('<int:pk>/update/', ContactUpdateView.as_view(), name='ContactUpdate'),
    path('<int:pk>/delete/', ContactDeleteView.as_view(), name='ContactDelete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='AssignAgent'),
    path('categories/', CategoryListView.as_view(), name='CategoryList'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='CategoryDetail'),
    path('<int:pk>/category/', ContactCategoryUpdateView.as_view(), name='ContactCategoryUpdate'),
]
