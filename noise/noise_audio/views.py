from django.shortcuts import render
from pydub import AudioSegment
import os
from .models import Audio
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .convert import converted


class NewStoryForm(LoginRequiredMixin, CreateView):
    """Add new story."""

    template_name = 'noise_audio/new_story.html'
    model = Audio
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('auth_login')
    fields = ['topic', 'path']

    def form_valid(self, form):
        """Validate form."""
        form.instance.creator = self.request.user
        file_path = form.instance.path
        form.instance.path = converted(file_path)
        form.save()
        form.instance.contributor.add(self.request.user)
        return super().form_valid(form)


class ContinueStoryForm(LoginRequiredMixin, UpdateView):
    """Add to existing story."""

    template_name = 'noise_audio/add_clip.html'
    model = Audio
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('auth_login')
    fields = ['path']
    context_object_name = 'story'
    slug_url_kwarg = 'clip_id'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        """Get context data."""
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        """Validate form."""
        form.instance.contributor.add(self.request.user)
        form.save()
        return super().form_valid(form)
