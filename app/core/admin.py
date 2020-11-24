from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

# Register your models here.
admin.site.unregister(Group)
admin.site.unregister(Site)