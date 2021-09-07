from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# we run the above function everytime new user created
# when a user is saved then it sends a signal
# and the signal is caught by the receiver
# create_profile is a receiver
# instance argument is an instance of a User
# if the user is created then we create a new profile
# attached to that user

def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# and after creation we have to save that profile
