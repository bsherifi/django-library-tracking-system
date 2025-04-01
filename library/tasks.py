from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    try:
        overdue_loans = Loan.objects.filter(is_returned=False, due_date__lt=now().date())

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