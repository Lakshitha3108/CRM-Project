import uuid

from . models import students

import string

import random



def get_admission_number():

    pattern = str(uuid.uuid4().int)[:7]

    admission_number = f'LM-{pattern}'

    if not students.objects.filter(adm_num=admission_number).exists():

        return admission_number

    # print(admission_number)

def get_password():

    password = random.choices(string.ascii_letters+string.digits)

    print(password)

get_password()

