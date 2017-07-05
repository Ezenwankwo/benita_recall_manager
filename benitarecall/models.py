from django.db import models
from datetime import date
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError



# Create your models here.
class Patient(models.Model):
	card_number = models.CharField(unique=True, max_length=50, blank=False)
	patient_name = models.CharField(max_length=100, help_text="Title Surname Firstname", blank=False)
	sex = (
		('Male', 'Male'),
		('Female', 'Female'),
	)

	sex = models.CharField(max_length=7, choices=sex, blank=False)
	date_of_birth = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>", null=True, blank=True)
	phone_number = models.CharField(max_length=30, blank=False)
	email = models.CharField(max_length=150, blank=True)
	address = models.CharField(max_length=200, blank=True)
	occupation = models.CharField(max_length=100, blank=True)
	hmo = models.CharField("HMO", max_length=200, help_text="Name of HMO(HMO ID Number)", blank=True)


	class Meta:
		ordering = ['card_number']

	def __str__(self):
		return self.patient_name

	def get_absolute_url(self):
		return reverse('benitarecall:patient_detail', kwargs={'pk': self.pk})


class Schedule(models.Model):
	patient = models.CharField("Patient Name", max_length=100, help_text="Surname  Firstname  Othername", blank=False)
	date_of_visit = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>", blank=False)
	summary_of_visit = models.TextField(max_length=500, blank=True)
	date_of_recall = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>", blank=False)
	reason_for_recall = models.TextField(max_length=200, blank=True)

	RECALL_STATUS = (
		('On Schedule', 'On Schedule'),
		('A Reminder', 'A Reminder'),
	)

	recall_status = models.CharField(max_length=15, choices=RECALL_STATUS, blank=True, default='On Schedule')




	class Meta:
		ordering = ['date_of_recall']
		

	def __str__(self):
		return self.patient

	def get_absolute_url(self):
		return reverse('benitarecall:detail_recall', kwargs={'pk': self.pk})

	def clean(self):
		date_of_recall = self.date_of_recall

		if date_of_recall < date.today():
			raise ValidationError('You cannot schedule a recall for the past. Please check your date')


	
	