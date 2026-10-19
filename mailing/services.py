from datetime import timezone

from django.core.mail import send_mail

from config import settings
from mailing.models import Mailing, MailingAttempt


def send_mailing(mailing_id):

    try:
        mailing = Mailing.objects.get(id=mailing_id)
    except Mailing.DoesNotExist:
        return {
            "success": False,
            "message": f"Рассылка с ID {mailing_id} не найдена",
            "sent_count": 0,
            "failed_count": 0,
        }

    now = timezone.now()
    if not (mailing.start_time <= now <= mailing.end_time):
        return {
            "success": False,
            "message": "Рассылка не может быть запущена",
            "sent_count": 0,
            "failed_count": 0,
        }

    recipients = mailing.recipients.all()
    if not recipients.exists():
        return {
            "success": False,
            "message": "У рассылки нет получателей",
            "sent_count": 0,
            "failed_count": 0,
        }

    sent_count = 0
    failed_count = 0

    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                status=MailingAttempt.STATUS_SUCCESS,
                server_response=f"Письмо отправлено на {recipient.email}",
            )
            sent_count += 1
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status=MailingAttempt.STATUS_FAILED,
                server_response=f"Письмо не может быть отправлено на  {recipient.email}, ошибка {str(e)}",
            )
            failed_count += 1

    return {
        "success": True,
        "message": f"Отправлено: {sent_count}, ошибок: {failed_count}",
        "sent_count": sent_count,
        "failed_count": failed_count,
    }
