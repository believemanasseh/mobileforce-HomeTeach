from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class Rating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rate = models.DecimalField(default=0.0, decimal_places=2, max_digits=5)


class Request(models.Model):
	requester = models.ForeignKey(User, related_name='pending_requests', on_delete=models.CASCADE)
	tutor = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
	description = models.CharField(max_length=1000)
	date_requested = models.DateTimeField(auto_now_add=True)
	accepted = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.requester.full_name} requests {self.tutor.full_name}'


# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,
							on_delete=models.CASCADE)
	rating = models.ManyToManyField(Rating, blank=True)
	profile_pic = models.FileField(blank=True, null=True)
	desc = models.CharField(max_length=255, null=True, blank=True)
	field = models.CharField(max_length=255, null=True, blank=True)
	major_course = models.CharField(max_length=255, null=True, blank=True)
	other_courses = models.CharField(max_length=255, null=True, blank=True)
	state = models.CharField(max_length=255, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	

	def __unicode__(self):
		return f'Profile for user: {self.user.email}'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

