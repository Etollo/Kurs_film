from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from account.forms import UserUpdateForm
from account.models import CustomUser
from django.views.generic import View
from django.db.models import Q
from django.core import serializers
from reviewer.utils import ObjectUpdateMixin, ObjectCreateMixin, ObjectDeleteMixin


class UserList(View):
    nbar = 'users'

    def get(self, request):
        # users = get_object_or_404(CustomUser, company=request.user.company.id)
        users = CustomUser.objects.filter(Q(company=request.user.company.id) | Q(company__parent=request.user.company.id))
        print(users)
        return render(request, 'administration/user_list.html', context={'users': users, 'nbar': self.nbar})


@login_required
def user_json(request):
    users = CustomUser.objects.filter(Q(company=request.user.company.id) | Q(company__parent=request.user.company.id))
    json = serializers.serialize('json', users)
    return HttpResponse(json, content_type='application/json')


class UserDetail(ObjectUpdateMixin, View):
    model = CustomUser
    template = 'administration/user_detail.html'
    nbar = 'users'


class UserCreate(ObjectCreateMixin, View):
    model_form = CustomUser
    template = 'administration/user_create.html'
    nbar = 'users'


class UserUpdate(ObjectUpdateMixin, View):
    model = CustomUser
    model_form = UserUpdateForm
    template = 'administration/user_update.html'
    nbar = 'users'


class UserDelete(ObjectDeleteMixin, View):
    model = CustomUser
    template = 'administration/user_delete.html'
    redirect_url = 'user_list_url'
    nbar = 'users'