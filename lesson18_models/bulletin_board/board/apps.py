from django.apps import AppConfig


class BoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board'
    verbose_name = 'Дошка оголошень'

    def ready(self) -> None:
        """
        Виконується при готовності застосунку.
        Імпортує сигнали для їх реєстрації.
        """
        from . import signals
