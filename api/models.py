from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # current user model


class Component(models.Model):
    """
    The component that can be used as a part of a construction.
    A client can choose the the components he want and assemble
    the construction he wish.

    For example, if you want to have a chair, you should have
    such components like legs, frame, seat and back.
    """
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    image = models.ImageField(blank=True, upload_to='componentImages/')
    description = models.TextField()
    manufacturer = models.CharField(max_length=25)
    rating = models.IntegerField()
    category = models.CharField(max_length=25)
    type = models.CharField(max_length=30)
    weight = models.FloatField()


class ComponentReport(models.Model):
    """
    A user's impression of the component, the experience he has using it.
    A comment where client can describe all pros and cons which have been
    noticed by him, the general impression and advices to use it or not.
    """
    #id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    component = models.ForeignKey(Component, on_delete=models.CASCADE)


class WebStore(models.Model):
    """
    The store which has provided the list of the goods it sells.
    """
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    logo = models.ImageField()
    homepage = models.URLField()


class WebStoreComponent(models.Model):
    """
    The data provided by a store about a component it sells.
    """
    web_store = models.ForeignKey(WebStore, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    component_page_link = models.URLField()


class AssembledConstruction(models.Model):
    """
    The construction which consists of a set of components and can fulfil
    the role it was assembled for.
    Contains it's schema and the step-by-step instruction how it can be assembled.
    """
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(blank=True, upload_to='constructionsImages/')
    rating = models.IntegerField()
    schema = models.ImageField(blank=True, upload_to='schemas/')
    assemble_instruction = models.FileField(blank=True, upload_to='instructions/')
    instruction_images = models.FileField(blank=True, upload_to='instructions/')


class ConstructionComponent(models.Model):
    """
    A certain component which a certain construction contains.
    """
    component = models.ForeignKey(Component,
                                  on_delete=models.CASCADE)
    construction = models.ForeignKey(AssembledConstruction,
                                     on_delete=models.CASCADE)

    class Meta:
        unique_together = ('component_id', 'construction_id')


class ConstructionReport(models.Model):
    """
    A user's impression of the construction, the experience he has using it.
    A comment where client can describe all pros and cons which have been
    noticed by him during this construction exploitation, the design flaws
    that have been detected, the general impression and advices to use it or not.
    """
    #id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    construction = models.ForeignKey(AssembledConstruction,
                                     on_delete=models.CASCADE)


class Cart(models.Model):
    """
    The goods such as construction schemas that a current user want to buy
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    construction = models.ForeignKey(AssembledConstruction,
                                     on_delete=models.CASCADE)


class UserConstruction(models.Model):
    """
    The goods such as construction schemas that a current user want to buy
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    construction = models.ForeignKey(AssembledConstruction,
                                     on_delete=models.CASCADE)