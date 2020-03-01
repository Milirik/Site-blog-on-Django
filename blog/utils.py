from django.shortcuts import render, get_object_or_404, redirect, reverse

class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request,
                      self.template,
                      context={self.model.__name__.lower(): obj, 'admin_object': obj, 'detail': True})


class ObjectCreateMixin:
    modelForm = None
    template = None

    def get(self, request):
        form = self.modelForm()
        return render(request,
                      self.template,
                      context={'form':form})

    def post(self, request):
        bound_form = self.modelForm(request.POST)

        if bound_form.is_valid():
            new = bound_form.save()
            return redirect(new)
        return render(request,
                      self.template,
                      context={'form':bound_form})


class ObjectsUpdateMixin:
    model = None
    modelForm = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.modelForm(instance=obj)
        return render(request,
                      self.template,
                      context={'form':bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.modelForm(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request,
                      'blog/tag_update_form.html',
                      context={'form':bound_form, self.model.__name__.lower(): obj})



class ObjectDeleteMixin:
    model = None
    template = None
    template_of_list = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request,
                      self.template,
                      context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.template_of_list))

