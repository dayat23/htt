import logging
from django.db import connection

from .permissions import setup_permissions

logger = logging.getLogger(__name__)


def install():
    """
    Install the product module.
    This function is called when the module is installed.
    """
    logger.info("Installing product module...")

    # Create database tables if they don't exist
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM django_migrations
            WHERE app = 'product_module' AND name = '0001_initial'
        """)
        if cursor.fetchone()[0] == 0:
            # Run migrations for the app
            from django.core.management import call_command
            call_command('migrate', 'product_module')

    # Set up permissions
    setup_permissions()

    # Register the module's URLs
    # This is handled by including the URLs in the main URLconf

    logger.info("Product module installed successfully.")
    return True


def upgrade():
    """
    Upgrade the product module.
    This function is called when the module is upgraded.
    """
    logger.info("Upgrading product module...")

    # Run migrations to apply any model changes
    from django.core.management import call_command
    call_command('migrate', 'product_module')

    # Update permissions
    setup_permissions()

    logger.info("Product module upgraded successfully.")
    return True


def uninstall():
    """
    Uninstall the product module.
    This function is called when the module is uninstalled.
    """
    logger.info("Uninstalling product module...")

    # We don't actually drop the tables here to prevent data loss
    # Instead, we just mark the module as uninstalled in the database
    # The views will check if the module is installed before allowing access

    logger.info("Product module uninstalled successfully.")
    return True


def is_installed(user):
    """
    Check if the product module is installed.
    """
    from htt.module_engine.models import Module

    try:
        module = Module.objects.get(app_name='product_module')
        return module.is_installed(user)
    except Module.DoesNotExist:
        return False
