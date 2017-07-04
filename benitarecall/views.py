from django.conf import settings
from django.db.models import Q
from datetime import date 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy 
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render
from benitarecall.models import Patient
from benitarecall.models import Schedule


# Create your views here.

class PatientFormView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

	model = Patient
	template_name = 'benitarecall/add_patient.html'
	fields = ['card_number', 'patient_name', 'sex', 'date_of_birth', 'phone_number', 'email', 'address', 'occupation', 'hmo']
	success_url = reverse_lazy('benitarecall:add_patient')
	success_message = 'Patient successfully added'


class PatientListView(LoginRequiredMixin, ListView):

	model = Patient
	template_name = 'benitarecall/list_patient.html'
	context_object_name = 'patients'
	paginate_by = 20

	def get_queryset(self, *args, **kwargs):
		queryset_list = Patient.objects.all()
		query = self.request.GET.get("q")
		
		if query:
			queryset_list = queryset_list.filter(
				Q(card_number__icontains=query)|
				Q(patient_name__icontains=query)
				).distinct()
		return queryset_list



class PatientDetailView(DetailView):

	model = Patient
	template_name = 'benitarecall/detail_patient.html'
	context_object_name = 'patients'

class PatientDeleteView(SuccessMessageMixin, DeleteView):

	model = Patient
	template_name = 'benitarecall/delete_patient.html'
	success_url = reverse_lazy('benitarecall:patient_list')


class PatientUpdateView(SuccessMessageMixin, UpdateView):

	model = Patient
	template_name = 'benitarecall/update_patient.html'
	fields = ['card_number', 'patient_name', 'sex', 'date_of_birth', 'phone_number', 'email', 'address', 'occupation', 'hmo']
	success_url = reverse_lazy('benitarecall:patient_list') 
	
class CreateScheduleView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    #Powers a form to create a new recall

	model = Schedule
	template_name = 'benitarecall/create_recall.html'
	fields = ['patient', 'date_of_visit', 'summary_of_visit', 'date_of_recall', 'reason_for_recall', 'recall_status']
	success_url = reverse_lazy('benitarecall:create_recall')
	success_message = 'Recall successfully created'


class ViewScheduleView(LoginRequiredMixin, ListView):

	#Shows users a list of appointments.  

	model = Schedule
	template_name = 'benitarecall/view_recall.html'
	context_object_name = 'view_recall' 
	paginate_by = 20
	queryset_list = Schedule.objects.exclude(date_of_recall__lt=date.today())

	
	def get_queryset(self, *args, **kwargs):
		queryset_list = Schedule.objects.exclude(date_of_recall__lt=date.today())
		query = self.request.GET.get("q")
		
		if query:
			queryset_list = queryset_list.filter(
				Q(date_of_recall__icontains=query)|
				Q(patient__icontains=query)
				).distinct()
		return queryset_list


class PastRecallView(ListView):

	model = Schedule
	template_name = 'benitarecall/past_recall.html'
	context_object_name = 'past_recall'
	paginate_by = 20
	queryset_list = Schedule.objects.filter(date_of_recall__lt=date.today())


	def get_queryset(self, *args, **kwargs):
		queryset_list = Schedule.objects.filter(date_of_recall__lt=date.today())
		query = self.request.GET.get("q")
		
		if query:
			queryset_list = queryset_list.filter(
				Q(date_of_recall__icontains=query)|
				Q(patient__icontains=query)
				).distinct()
		return queryset_list


	
class ScheduleDetailView(DetailView):

	#Shows users a single appointment

	model = Schedule
	template_name = 'benitarecall/detail_recall.html'
	context_object_name = 'schedule'

class ScheduleUpdateView(SuccessMessageMixin, UpdateView):
	#powers a form to edit existing recall

	model = Schedule
	template_name = 'benitarecall/schedule_form.html'
	fields = ['patient', 'date_of_visit', 'summary_of_visit', 'date_of_recall', 'reason_for_recall', 'recall_status']
	success_url = reverse_lazy('benitarecall:view_recall')
	success_message = 'Recall successfully updated'



class ScheduleDeleteView(SuccessMessageMixin, DeleteView):
	#prompts user to confirm deletion of a recall

	model = Schedule
	success_url = reverse_lazy('benitarecall:view_recall')