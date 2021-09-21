from django.db import models
from django.contrib.auth.models import User
from .choices import perfil
# Create your models here.

class funcionario(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perfil = models.CharField( max_length=25, choices=perfil)

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(self):
        return str(self.user.first_name +' '+self.user.last_name )
