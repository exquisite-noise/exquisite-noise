from django.urls import path
from .views import (
    NewStoryForm
    )

urlpatterns = [
    path('new/', NewStoryForm.as_view(create_field='audio_file'), name='new'),
]
