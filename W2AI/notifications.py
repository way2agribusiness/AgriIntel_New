from django.core.mail import send_mail

def send_notification(subject,message,recipient_list):
    send_mail(subject,message,'contact@way2agribusiness.com',recipient_list, html_message=message)

