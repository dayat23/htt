from django.urls import path

from . import views

app_name = "module_engine"

urlpatterns = [
    path("", views.ModulListView.as_view(), name="module_list"),
    path("install/<int:pk>/", views.InstallModulView.as_view(), name="install_module"),
    path("upgrade/<int:pk>/", views.UpgradeModulView.as_view(), name="upgrade_module"),
    path("uninstall/<int:pk>/", views.UninstallModulView.as_view(), name="uninstall_module"),
]
