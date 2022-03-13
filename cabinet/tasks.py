import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from django.conf import settings
from sendgrid import SendGridAPIClient, TemplateId, DynamicTemplateData
from sendgrid.helpers.mail import Mail
from django.shortcuts import get_object_or_404

from .models import Response
from insure_bro.celery import app


@app.task(name="sendmail", autoretry_for=(Exception,), retry_kwargs={'max_retries': 5, 'countdown': 10})
def send_email(response_id):
    response = get_object_or_404(Response, id=response_id)
    email_company = response.product.company.email
    date = f"{datetime.today().day}.{datetime.today().month}.{datetime.today().year}"
    subject = "Пока тест"
    html_message = render_to_string("cabinet/email.html", {"response": response, "date": date})
    message = strip_tags(html_message)
    message = "Возьмите страховку"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email_company], html_message=html_message)
