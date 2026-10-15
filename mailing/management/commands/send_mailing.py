from django.core.management import BaseCommand
from mailing.services import send_mailing


class Command(BaseCommand):
    help = "Запускает рассылку по её ID"

    def add_arguments(self, parser):
        parser.add_arguments("mailing_id", type=int, help="ID рассылки")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]

        self.stdout.write(f"Запуск рассылки #{mailing_id}...")

        result = send_mailing(mailing_id)

        if result["success"]:
            self.stdout.write(self.style.SUCCESS(f"{result['message']}"))

        else:
            self.stdout.write(self.style.ERROR(f"{result['message']}"))
