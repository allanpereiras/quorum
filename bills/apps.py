from django.apps import AppConfig


class BillsConfig(AppConfig):
    """
    This is the AppConfig class for the 'bills' application.

    This application provides functionalities related to visualizing all of
    the bills that legislators voted for or against.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "bills"
    verbose_name = "Legislature bills voting"
