from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None
    nbar = None

    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        bound_form = self.model_form(company=request.user.company_id, instance=obj)
        return render(request, self.template,
                      context={'form': bound_form, self.model.__name__.lower(): obj, 'nbar': self.nbar})

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        bound_form = self.model_form(company=request.user.company_id, data=request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)

        return render(request, self.template,
                      context={'form': bound_form, self.model.__name__.lower(): obj, 'nbar': self.nbar})