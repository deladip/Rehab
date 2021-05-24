from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Emp

def emp_profile(sender, instance, created, **kwargs)
    if created:
        group = Group.objects.get(name='emp')
        instance.groups.add(group)
        Emp.objects.create(
            user=instance,
            name=instance.username
            )
        print('Profile Created!')

post_save.connect(emp_profile, sender=User)
