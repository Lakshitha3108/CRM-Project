import uuid

from . models import students

import string

import random


from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from django.conf import settings



def get_admission_number():

    pattern = str(uuid.uuid4().int)[:7]

    admission_number = f'LM-{pattern}'

    if not students.objects.filter(adm_num=admission_number).exists():

        return admission_number

    # print(admission_number)

def get_password():

    password = ''.join(random.choices(string.ascii_letters+string.digits,k=8))

    return password


#email sending 

def send_email(subject,recepients,template,context):

    email_obj = EmailMultiAlternatives(subject,from_email=settings.EMAIL_HOST_USER,to=recepients)

    content = render_to_string(template,context)

    email_obj.attach_alternative(content,'text/html')

    email_obj.send()




