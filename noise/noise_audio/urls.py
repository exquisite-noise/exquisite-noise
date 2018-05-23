from django.urls import path
from .views import (
    NewStoryForm,
    ContinueStoryForm
    )

urlpatterns = [
    path('add/<int:clip_id>/', ContinueStoryForm.as_view(), name='add'),
    path('new/', NewStoryForm.as_view(create_field='audio_file'), name='new'),
]
