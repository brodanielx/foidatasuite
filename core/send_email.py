import os
from email.mime.image import MIMEImage


from django.conf import settings
from django.core.mail import EmailMultiAlternatives



def send_email(subject, recipient_list, text_content, html_content=None, attachments=None):
    
    if settings.DEBUG:
        recipient_list = ['foitampa.automate@gmail.com']

    from_email = settings.EMAIL_HOST_USER

    msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            recipient_list,
        )

    if html_content:
        msg.attach_alternative(html_content, "text/html")

        msg.mixed_subtype = 'related'

        
        static_images = ['noiflagcircle.png']

        for f in static_images:
            path = os.path.join(settings.STATIC_ROOT, f)
            fp = open(path, 'rb')
            msg_img = MIMEImage(fp.read())
            fp.close()
            msg_img.add_header('Content-ID', f'<{f}>')
            msg.attach(msg_img)

    msg.send()