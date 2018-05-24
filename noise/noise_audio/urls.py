from django.urls import path
from .views import (
    NewStoryForm,
    LinkView,
    ContinueStoryForm
    )

urlpatterns = [
    path('new/', NewStoryForm.as_view(create_field='audio_file'), name='new'),
    path('link/', LinkView.as_view(), name='link'),
    path('add/<int:clip_id>/', ContinueStoryForm.as_view(
        create_field='audio_file'), name='add'),
]
