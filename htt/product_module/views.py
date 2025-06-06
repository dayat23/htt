from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Product
from .forms import ProductForm
from .permissions import has_product_permission, get_user_role
from .module_utils import is_installed


class ProductListView(LoginRequiredMixin, ListView):
    template_name = "product_module/product_list.html"
    model = Product
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        # Check if module is installed
        if not is_installed():
            messages.error(request, _("The Product module is not installed."))
            return HttpResponseRedirect(reverse("home"))

        # Check if user has permission to view products
        if not has_product_permission(request.user, "view_product"):
            messages.error(request, _("You don't have permission to view products."))
            return HttpResponseRedirect(reverse("home"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list = None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["user_role"] = get_user_role(self.request.user)
        return ctx


class ProductDetailView(LoginRequiredMixin, DetailView):
    template_name = "product_module/product_detail.html"
    model = Product
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        # Check if module is installed
        if not is_installed():
            messages.error(request, _("The Product module is not installed."))
            return HttpResponseRedirect(reverse("home"))

        # Check if user has permission to view products
        if not has_product_permission(request.user, "view_product"):
            messages.error(request, _("You don't have permission to view products."))
            return HttpResponseRedirect(reverse("product_module:product_list"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list = None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["user_role"] = get_user_role(self.request.user)
        return ctx


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = "product_module/product_form.html"
    model = Product
    form_class = ProductForm
    queryset = Product.objects.all()
    extra_context = {"form_type": "create"}

    def get(self, request, *args, **kwargs):
        # Check if module is installed
        if not is_installed():
            messages.error(request, _("The Product module is not installed."))
            return HttpResponseRedirect(reverse("home"))

        # Check if user has permission to view products
        if not has_product_permission(request.user, "view_product"):
            messages.error(request, _("You don't have permission to view products."))
            return HttpResponseRedirect(reverse("product_module:product_list"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list = None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["user_role"] = get_user_role(self.request.user)
        return ctx

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, _("Product created successfully."))
        return HttpResponseRedirect(reverse("product_module:product_detail", kwargs={"pk": self.object.id}))


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "product_module/product_form.html"
    model = Product
    form_class = ProductForm
    queryset = Product.objects.all()
    extra_context = {"form_type": "update"}

    def get(self, request, *args, **kwargs):
        # Check if module is installed
        if not is_installed():
            messages.error(request, _("The Product module is not installed."))
            return HttpResponseRedirect(reverse("home"))

        # Check if user has permission to view products
        if not has_product_permission(request.user, "view_product"):
            messages.error(request, _("You don't have permission to view products."))
            return HttpResponseRedirect(reverse("product_module:product_list"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list = None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["user_role"] = get_user_role(self.request.user)
        return ctx

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, _("Product updated successfully."))
        return HttpResponseRedirect(reverse("product_module:product_detail", kwargs={"pk": self.object.id}))


class ProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "product_module/product_confirm_delete.html"
    model = Product
    success_message = _("Product deleted successfully.")
    success_url = reverse_lazy("product_module:product_list")

    def get(self, request, *args, **kwargs):
        # Check if module is installed
        if not is_installed():
            messages.error(request, _("The Product module is not installed."))
            return HttpResponseRedirect(reverse("home"))

        # Check if user has permission to view products
        if not has_product_permission(request.user, "view_product"):
            messages.error(request, _("You don't have permission to view products."))
            return HttpResponseRedirect(reverse("product_module:product_list"))

        return super().get(request, *args, **kwargs)


@login_required
def product_delete_confirm(request, pk):
    """
    AJAX view to confirm product deletion.
    """
    # Check if module is installed
    if not is_installed():
        return JsonResponse({"success": False, "message": _("The Product module is not installed.")})

    # Check if user has permission to delete products
    if not has_product_permission(request.user, "delete_product"):
        return JsonResponse({"success": False, "message": _("You don't have permission to delete products.")})

    if request.method == "POST":
        try:
            product = get_object_or_404(Product, id=pk)
            product.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": _("Invalid request method.")})
