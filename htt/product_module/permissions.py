from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from .models import Product


def setup_permissions():
    """
    Set up the permissions for the Product model.
    Create the necessary groups and assign permissions.
    """
    # Get content type for the Product model
    content_type = ContentType.objects.get_for_model(Product)

    # Create permissions if they don't exist
    view_permission, _ = Permission.objects.get_or_create(
        codename="view_product",
        content_type=content_type,
        defaults={"name": "Can view product"}
    )
    add_permission, _ = Permission.objects.get_or_create(
        codename="add_product",
        content_type=content_type,
        defaults={"name": "Can add product"}
    )
    change_permission, _ = Permission.objects.get_or_create(
        codename="change_product",
        content_type=content_type,
        defaults={"name": "Can change product"}
    )
    delete_permission, _ = Permission.objects.get_or_create(
        codename="delete_product",
        content_type=content_type,
        defaults={"name": "Can delete product"}
    )

    # Create groups if they don't exist
    manager_group, _ = Group.objects.get_or_create(name="product_manager")
    user_group, _ = Group.objects.get_or_create(name="product_user")
    public_group, _ = Group.objects.get_or_create(name="product_public")

    # Assign permissions to groups
    # Manager: CRUD
    manager_group.permissions.add(view_permission, add_permission, change_permission, delete_permission)

    # User: CRU
    user_group.permissions.add(view_permission, add_permission, change_permission)

    # Public: R
    public_group.permissions.add(view_permission)


def has_product_permission(user, permission_codename):
    """
    Check if the user has the specified permission for the Product model.
    """
    if user.is_superuser:
        return True

    # Get the permission
    content_type = ContentType.objects.get_for_model(Product)
    permission = Permission.objects.filter(
        content_type=content_type,
        codename=permission_codename
    ).first()

    if not permission:
        return False

    # Check if the user has the permission directly or through a group
    return user.has_perm(f"{content_type.app_label}.{permission_codename}")


def get_user_role(user):
    """
    Get the role of the user based on their group membership.
    Returns 'manager', 'user', 'public', or None.
    """
    if user.is_superuser:
        return 'manager'

    if user.groups.filter(name="product_manager").exists():
        return 'manager'
    elif user.groups.filter(name="product_user").exists():
        return 'user'
    elif user.groups.filter(name="product_public").exists() or user.is_authenticated:
        return 'public'

    return None
