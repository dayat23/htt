from django.urls import path

from . import views

app_name = "module_engine"

urlpatterns = [
    path("", views.ModulListView.as_view(), name="module_list"),
    path("install/<int:module_id>/", views.InstallModulView.as_view(), name="install_module"),
    path("upgrade/<int:module_id>/", views.UpgradeModulView.as_view(), name="upgrade_module"),
    path("uninstall/<int:module_id>/", views.UninstallModulView.as_view(), name="uninstall_module"),
]
