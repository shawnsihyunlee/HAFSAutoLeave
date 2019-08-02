from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Tutorial(models.Model):
	tutorial_title = models.CharField(max_length = 200)
	tutorial_content = models.TextField()
	tutorial_published = models.DateTimeField("date published")

	def __str__(self):
		return self.tutorial_title

class GoingInfo(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True,)
	do_auto_signup = models.BooleanField(default = False)
	student_id = models.CharField(max_length = 5, default = "00000")
	student_pass = models.CharField(max_length = 30, default = "00000")
	out_day = models.CharField(max_length = 10, default = "Friday")
	out_hour = models.IntegerField(default = 19)
	out_minute = models.IntegerField(default =00)
	return_day = models.CharField(max_length = 10, default = "Sunday")
	return_hour = models.IntegerField(default = 23)
	return_minute = models.IntegerField(default = 00)

	def __str__(self):
		return self.user.username + " information"


@receiver(post_save, sender=User)
def create_goinginfo(sender, instance, created, **kwargs):
	if created:
		GoingInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_goinginfo(sender, instance, **kwargs):
	instance.goinginfo.save()


