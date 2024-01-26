from django.db import models


# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=32, verbose_name='标题')
    def __str__(self):
        return self.title


class Userinfo(models.Model):
    name = models.CharField(max_length=16, verbose_name='姓名')
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='账户余额', default=0)
    create_time = models.DateField(verbose_name='入职时间')

    depart = models.ForeignKey(to="Department", to_field="id", verbose_name='部门', on_delete=models.CASCADE)

    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(choices=gender_choices, verbose_name='性别')
