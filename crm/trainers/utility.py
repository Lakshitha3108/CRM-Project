import uuid

from . models import Trainers

import string

import random

# LM-1000101

def get_employee_id():

    while True:

        pattern = str(uuid.uuid4().int)[:7]

        employee_num = f'LM-E{pattern}'

        if not Trainers.objects.filter(employee_id=employee_num).exists():             # ORM

            return employee_num
        
def get_password():

    password = ''.join(random.choices(string.ascii_letters + string.digits,k=8))

    return password