from django.apps import AppConfig


class IntegracoesConfig(AppConfig):
    name = 'integracoes'
    def ready(self):
        import integracoes.signals