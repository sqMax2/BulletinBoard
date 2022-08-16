from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.db import transaction

from .models import Category, Post, Message
from b_board.settings import DEFAULT_FROM_EMAIL


@receiver(post_save, sender=Message)
def notify_author(sender, instance, **kwargs):
    redirectURL = f'http://127.0.0.1:8000{instance.get_absolute_url()}'
    if instance.status:
        mail = instance.author.email
        subject = 'Your message was accepted'
        body = f'Your message replying post {instance.post.title} was accepted.'
        html_content = render_to_string(
            'mail_msg_accept.html',
            {
                'post': instance,
                'redirectURL': redirectURL,
            }
        )

        # send_mail(
        #     'Your message was accepted',
        #     f'Your <a href=http://127.0.0.1:8000/{instance.get_absolute_url()}>message</a> replying post '
        #     f'<i>{instance.post.title}</i> was accepted.',
        #     f'{DEFAULT_FROM_EMAIL}',
        #     [mail],
        #     fail_silently=False,
        # )
        # return
    else:
        mail = instance.post.author.email
        subject = 'You have a new message'
        body = f'You have a new reply on Your post {instance.post.title}.'
        html_content = render_to_string(
            'mail_msg_reply.html',
            {
                'post': instance,
                'redirectURL': redirectURL,
            }
        )
    # send_mail(
    #     'You have a new message',
    #     f'You have a new <a href=http://127.0.0.1:8000/{instance.get_absolute_url()}>reply</a> on Your post '
    #     f'<i>{instance.post.title}</i>.',
    #     f'{DEFAULT_FROM_EMAIL}',
    #     [mail],
    #     fail_silently=False,
    # )
    print(f'sending email to {mail}')
    msg = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=DEFAULT_FROM_EMAIL,
        to=[mail]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
