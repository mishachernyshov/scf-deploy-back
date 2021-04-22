from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Component, ComponentReport, WebStore, \
    WebStoreComponent, AssembledConstruction, ConstructionComponent, \
    ConstructionReport, Cart

my_models = [Component, ComponentReport, WebStore,
             WebStoreComponent, AssembledConstruction,
             ConstructionComponent, ConstructionReport, Cart]
admin.site.register(my_models)
admin.site.unregister(Group)