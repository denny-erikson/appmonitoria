from django.apps import AppConfig

class MonitoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoria'

    def ready(self):
        # Importa os sinais para registrá-los
        import monitoria.signals
