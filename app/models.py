from django.db import models
from django.urls import reverse
from django.utils import timezone


class Menu(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название меню")
    slug = models.SlugField(max_length=255, verbose_name='Slug', null=True)
    named_url = models.CharField(max_length=255, verbose_name='Named URL', blank=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name

    def get_full_path(self):
        if self.named_url:
            url = reverse(self.named_url)
        else:
            url = '/{}/'.format(self.slug)
        return url


class MenuItem(models.Model):
    """
    Model for menu item. Has menu, parent, title, url fields.
    Menu field is only requied for top level items.
    You can provide any item in parent field and it will become relative for this item.
    If you'll use 'named url' field, get_url method will use it firstly to generate url.
    And only then 'url' field.
    """
    menu = models.ForeignKey(Menu, related_name='items',
                             verbose_name='menu', blank=True, null=True,
                             on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='items',
                               verbose_name='parent menu item',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Item title')
    url = models.CharField(max_length=255, verbose_name='Link', blank=True)
    named_url = models.CharField(max_length=255, verbose_name='Named URL', blank=True)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def get_url(self):
        if self.named_url:
            url = reverse(self.named_url)
        elif self.url:
            url = self.url
        else:
            url = '/'

        return url

    def __str__(self):
        return self.title
