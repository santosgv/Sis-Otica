"""
Notificacoes/management/commands/enviar_lembretes_anuais.py

O lembrete anual não é disparado por um evento de OS — é um job periódico.
Rode diariamente via cron (ou tarefa agendada equivalente no seu ambiente):

    python manage.py enviar_lembretes_anuais

Exemplo de crontab (todo dia às 9h):
    0 9 * * * cd /caminho/do/projeto/Backend && /caminho/venv/bin/python manage.py enviar_lembretes_anuais >> /var/log/lembretes_anuais.log 2>&1

Lógica: para cada cliente, pega a OS mais recente com STATUS em ('F', 'E')
(finalizada ou entregue) e DATA_ENCERRAMENTO preenchida. Se essa data caiu
entre 365 e 372 dias atrás (janela de ~1 semana, pra cobrir o cron rodando
diariamente sem perder o "aniversário"), e ainda não existe
LembreteAnualEnviado para essa OS, envia e registra.
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Max
from django.utils import timezone

from Core.models import ORDEN
from integracoes.models import LembreteAnualEnviado, WhatsAppConfig
from integracoes.service import (
    WhatsAppAPIError,
    WhatsAppConfigError,
    mensagem_lembrete_anual,
)

JANELA_DIAS_MIN = 365
JANELA_DIAS_MAX = 372  # ~1 semana de folga para o cron não perder a data


class Command(BaseCommand):
    help = (
        'Envia lembrete anual de exame para clientes cuja última OS '
        'entregue/finalizada completou ~1 ano.'
    )

    def handle(self, *args, **options):
        config = WhatsAppConfig.objects.filter(
            ativo=True, notif_lembrete_anual=True
        ).first()

        if not config:
            self.stdout.write(self.style.WARNING(
                'Nenhuma WhatsAppConfig ativa com lembrete anual habilitado. Nada a fazer.'
            ))
            return

        if not config.esta_conectado:
            self.stdout.write(self.style.WARNING(
                f'Instância "{config.instance_name}" não está conectada. Abortando.'
            ))
            return

        hoje = timezone.now().date()
        janela_inicio = hoje - timedelta(days=JANELA_DIAS_MAX)
        janela_fim = hoje - timedelta(days=JANELA_DIAS_MIN)

        # última data de encerramento por cliente
        ultimas_por_cliente = (
            ORDEN.objects.filter(STATUS__in=['F', 'E'], DATA_ENCERRAMENTO__isnull=False)
            .values('CLIENTE')
            .annotate(ultima_data=Max('DATA_ENCERRAMENTO'))
        )

        enviados = 0
        pulados = 0

        for item in ultimas_por_cliente:
            ultima_data = item['ultima_data'].date()
            if not (janela_inicio <= ultima_data <= janela_fim):
                continue

            ordem = (
                ORDEN.objects.filter(
                    CLIENTE_id=item['CLIENTE'],
                    DATA_ENCERRAMENTO__date=ultima_data,
                )
                .order_by('-id')
                .first()
            )
            if not ordem:
                continue

            if LembreteAnualEnviado.objects.filter(ordem=ordem).exists():
                pulados += 1
                continue

            try:
                mensagem_lembrete_anual(config.instance_name, ordem)
                config.registrar_envio()
                LembreteAnualEnviado.objects.create(ordem=ordem)
                enviados += 1
                self.stdout.write(f'Lembrete enviado: OS #{ordem.pk} — {ordem.CLIENTE.NOME}')
            except WhatsAppConfigError as e:
                self.stderr.write(self.style.WARNING(
                    f'OS #{ordem.pk}: {e}'
                ))
            except WhatsAppAPIError as e:
                self.stderr.write(self.style.ERROR(
                    f'OS #{ordem.pk}: falha na API — {e}'
                ))

        self.stdout.write(self.style.SUCCESS(
            f'{enviados} lembrete(s) enviado(s), {pulados} já haviam sido enviados antes.'
        ))