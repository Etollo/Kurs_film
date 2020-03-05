from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

# Create your views here.

from django.urls import reverse


class ObjectDetailMixin:
    model = None
    template = None
    nbar = None

    def get(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'nbar': self.nbar})


class ObjectCreateMixin:
    model_form = None
    template = None
    nbar = None

    def get(self, request):
        form = self.model_form(office=request.user.office_id)
        return render(request, self.template, context={'form': form, 'nbar': self.nbar})

    def post(self, request):
        bound_form = self.model_form(office=request.user.office_id, data=request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None
    nbar = None

    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        bound_form = self.model_form(office=request.user.office_id, instance=obj)
        return render(request, self.template,
                      context={'form': bound_form, self.model.__name__.lower(): obj, 'nbar': self.nbar})

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        bound_form = self.model_form(office=request.user.office_id, data=request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)

        return render(request, self.template,
                      context={'form': bound_form, self.model.__name__.lower(): obj, 'nbar': self.nbar})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None
    nbar = None

    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'nbar': self.nbar})

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        obj.delete()

        return redirect(reverse(self.redirect_url))
