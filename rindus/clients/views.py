"""Clients views."""

# Django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

# Forms
from rindus.clients.forms import ClientForm

# Models
from rindus.clients.models import Client


class ClientsFeedView(LoginRequiredMixin, ListView):
    """Return all created clients."""

    template_name = 'clients/feed.html'
    model = Client
    ordering = ('-created',)
    paginate_by = 30
    context_object_name = 'clients'

    def get_context_data(self, **kwargs):
        context = super(ClientsFeedView, self).get_context_data(**kwargs)
        context['clients_filter'] = Client.objects.all()
        return context

    def get_queryset(self):
        object_list = Client.objects.all()
        if self.request.GET.get('first_name'):
            first_name = self.request.GET.get('first_name')
            object_list = object_list.filter(first_name=first_name)
        if self.request.GET.get('last_name'):
            last_name = self.request.GET.get('last_name')
            print(object_list)
            object_list = object_list.filter(last_name=last_name)
            print(object_list)
        return object_list


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Return client detail."""

    template_name = 'clients/detail.html'
    queryset = Client.objects.all()
    context_object_name = 'client'


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Create a new client."""

    template_name = 'clients/new.html'
    form_class = ClientForm
    success_url = reverse_lazy('clients:feed')

    def get_context_data(self, **kwargs):
        """Add user to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:feed')

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)
            
class ClientUpdateView(UpdateView):
    """Update client view."""

    template_name = 'clients/update.html'
    model = Client
    fields = ['first_name', 'last_name', 'iban']

    success_url = reverse_lazy('clients:feed')

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)