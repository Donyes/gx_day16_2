from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01 import models


# Create your views here.
def depart_list(request):
    """"部门列表"""
    departs_list = models.Department.objects.all()
    return render(request, 'depart_list.html', {'departs_list': departs_list})


def depart_add(request):
    """添加部门"""
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    title = request.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect('/depart/list')


def depart_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list')


def depart_edit(request, nid):
    """修改部门"""
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_object': row_object})
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list')


def user_list(request):
    """"用户管理"""
    queryset = models.Userinfo.objects.all()
    # for obj in queryset:
    #     print(obj.id, obj.name, obj.password, obj.age, obj.account, obj.create_time.strftime("%Y-%m-%d"),
    #           obj.get_gender_display(), obj.depart.title)
    return render(request, "user_list.html", {'queryset': queryset})


# def user_add(request):
#     """"添加用户"""
#     form = UserModelForm()
#     return render(request, 'user_add.html', {'form':form})


from django import forms


class UserModelForm(forms.ModelForm):  # 创建一个继承forms.ModelForm的类
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:  # 创建Meta类
        model = models.Userinfo  # 把models.py里的类实例化过来
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]  # 取UserInfo中部分的类过来

        # # widgets控制插件以控制样式这个要一个个输入，不用它
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control", "placeholder": ""})
        # }

    def __init__(self, *args, **kwargs):  # 重新定义init方法
        super().__init__(*args, **kwargs)  # 执行父类的init方法
        for name, field in self.fields.items():  # 循环找到所有字段中的插件，给所有字段插件加上样式
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    """添加用户（Modelform)"""
    if request.method == 'GET':
        form = UserModelForm()  # 把我们创建的类实例化
        return render(request, 'user_model_form_add.html', {"form": form})
    # POST提交，必须数据校验
    form = UserModelForm(request.POST)
    if form.is_valid():  # 对fields中的字段逐一校验
        # 如果数据合法，保存到数据库model = models.Userinfo定义的这个表
        # print(form.cleaned_data)
        form.save()
        return redirect('/user/list')
    else:  # 校验失败（在页面上显示错误信息）
        # print(form.errors)
        return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """编辑页面"""
    row_obj = models.Userinfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html',{"form": form})

    form = UserModelForm(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/user/list')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    """删除用户"""
    models.Userinfo.objects.filter(id=nid).delete()
    return redirect('/user/list')