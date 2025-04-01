import os
from celery import Celery
from library.models import Loan
from django.core.mail import send_mail


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

app = Celery('library_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def check_overdue_loans():
    overdue_loans = Loan.objects.filter(is_returned=False, due_date__lt=now().date())

    try:
        # try here
        for loan in overdue_loans:
            send_mail(
                "Hey this book is overdue",
                "Please return this book by the due date",
                [loan.member.user.email],
                fail_silently=False,
            )
    except:
        # except here
        return f"Failed to send notifications for {len(overdue_loans)} overdue loans"

    return f"{len(overdue_loans)} overdue loans sent notifications"