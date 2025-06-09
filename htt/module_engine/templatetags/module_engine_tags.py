from django import template

register = template.Library()


@register.filter
def get_installation_status(module_engine, user) -> bool:
    return module_engine.is_installed(user)


@register.filter
def get_upgrading_status(module_engine, user) -> bool:
    return module_engine.is_upgrading(user)
