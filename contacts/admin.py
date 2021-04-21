from django.contrib import admin

from .models import Contact, Agent, Category


admin.site.register(Contact)

admin.site.register(Category)
