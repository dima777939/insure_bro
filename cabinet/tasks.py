import os
from datetime import datetime
from django.conf import settings
from sendgrid import SendGridAPIClient, TemplateId, DynamicTemplateData
from sendgrid.helpers.mail import Mail
from django.shortcuts import get_object_or_404

from .models import Response
from insure_bro.celery import app


@app.task(name="sendgrid")
def sendgrid_email(response_id):
    response = get_object_or_404(Response, id=response_id)
    to_email = response.product.company.email
    subject = (
        f"Отклик на страховое предложение в категории {response.product.category.name}"
    )
    data = {
        "category": response.product.category.name,
        "name_product": response.product.name,
        "price": str(response.product.price),
        "interest_rate": response.product.interest_rate,
        "period": response.product.period,
        "first_name": response.first_name,
        "last_name": response.last_name,
        "phone": response.phone,
        "email": response.email,
        "date": f"{datetime.today().year}.{datetime.today().month}.{datetime.today().day}",
    }
    message = Mail(
        from_email=settings.EMAIL_HOST_USER,
        to_emails=to_email,
        subject=subject,
    )
    message.template_id = TemplateId("d-976e00de6c504b29aa889ee9c224c997")
    message.dynamic_template_data = DynamicTemplateData(data)
    try:
        sg = SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
        response = sg.client.mail.send.post(request_body=message.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.args)
